import aspose.words as aw

def Convertir_pdf(suministro):
    # Función de conversión sincrónica para ejecutarla en un subproceso
    doc = aw.Document()
    builder = aw.DocumentBuilder(doc)
    builder.insert_image(suministro)
    pdf_filename = suministro.replace('.TIF', '.pdf')
    doc.save(pdf_filename)
    return pdf_filename

