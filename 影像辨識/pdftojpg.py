import sys, fitz, os, datetime

def pyMuPDF_fitz(pdfPath, imagePath, count):
    name = ["1","2","3","4","5","6","7","8","9","10"]
    tmp = int(count)
    pdfDoc = fitz.open(pdfPath)
    path = imagePath+'/'+count
    if not os.path.exists(path):
        os.mkdir(path)
    for pg in range(pdfDoc.pageCount):
        page = pdfDoc[pg]
        rotate = int(0)
        zoom_x = 4.1655      # 4.1655= 2550x3300
        zoom_y = 4.1655
        mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pix = page.getPixmap(matrix=mat, alpha=False)

        pix.writePNG(imagePath+'/'+count+'/'+name[pg]+'.jpg')
        
    photofilePath = imagePath + '/' + count
    w = open("./image/count.txt",'w')
    tmp += 1
    count = str(tmp)
    w.write(count)
    w.close
    return photofilePath