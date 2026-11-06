from PIL import Image
im1 = Image.open('kyc_documents/K01_gst_certificate.png')
print("K01 GST cert size:", im1.size)
im2 = Image.open('kyc_documents/K02_gst_certificate.png')
print("K02 GST cert size:", im2.size)
im3 = Image.open('kyc_documents/K03_gst_certificate.png')
print("K03 GST cert size:", im3.size)

