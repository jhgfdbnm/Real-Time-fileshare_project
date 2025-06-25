import subprocess
import os
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from .models import EncryptedFile
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from django.core.files.storage import default_storage
from django.utils import timezone

# ✅ Drag-and-drop upload form
def drag_upload(request):
    return render(request, 'drag_upload.html')

# ✅ Simple upload form view
def upload_form(request):
    return render(request, 'upload_form.html')

# ✅ Upload + scan + encrypt + versioning
@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        temp_path = default_storage.save(uploaded_file.name, uploaded_file)
        temp_file_path = default_storage.path(temp_path)

        # 🛡️ Step 1: Virus scan using ClamAV
        result = subprocess.run(['clamscan', temp_file_path], capture_output=True, text=True)
        if "Infected files: 1" in result.stdout:
            os.remove(temp_file_path)
            return JsonResponse({'error': 'File contains a virus and was rejected ❌'}, status=400)

        # 🔁 Step 2: File versioning
        existing_versions = EncryptedFile.objects.filter(file__icontains=uploaded_file.name)
        version_number = existing_versions.count() + 1

        # 🔐 Step 3: Encrypt
        key = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_EAX)
        with open(temp_file_path, 'rb') as f:
            data = f.read()
        ciphertext, tag = cipher.encrypt_and_digest(data)

        with open(temp_file_path, 'wb') as f:
            f.write(cipher.nonce + tag + ciphertext)

        # 💾 Step 4: Save encrypted file
        enc_file = EncryptedFile(
            file=temp_path,
            key=key,
            nonce=cipher.nonce,
            tag=tag,
            version=version_number
        )
        enc_file.save()

        return JsonResponse({
            'message': 'File uploaded, scanned, and encrypted ✅',
            'file_id': enc_file.id,
            'version': version_number
        })

    return JsonResponse({'error': 'No file uploaded'}, status=400)

# ✅ Download view with one-time + expiry check
def download_file(request, file_id):
    enc_file = get_object_or_404(EncryptedFile, id=file_id)

    # ⏳ Expiry check
    if timezone.now() > enc_file.expires_at:
        return JsonResponse({'error': 'This download link has expired ⏳'}, status=403)

    # 🔓 One-time download check
    if enc_file.has_been_downloaded:
        return JsonResponse({'error': 'This file has already been downloaded 🔓'}, status=403)

    file_path = enc_file.file.path
    with open(file_path, 'rb') as f:
        nonce = f.read(16)
        tag = f.read(16)
        ciphertext = f.read()

    cipher = AES.new(enc_file.key, AES.MODE_EAX, nonce=nonce)
    try:
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    except ValueError:
        return JsonResponse({'error': 'Decryption failed'}, status=500)

    # 💾 Save decrypted file temporarily
    temp_path = file_path + "_decrypted"
    with open(temp_path, 'wb') as f:
        f.write(plaintext)

    # 🔐 Mark as downloaded
    enc_file.has_been_downloaded = True
    enc_file.save()

    return FileResponse(open(temp_path, 'rb'), as_attachment=True, filename='decrypted_' + os.path.basename(file_path))


