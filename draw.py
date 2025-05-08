import matplotlib.pyplot as plt
import numpy as np
import sys
from sqlLib import SQL
from matplotlib.backends.backend_pdf import PdfPages


if len(sys.argv) < 2:
    print("Usage: python draw.py <filename>\nExample: python draw.py text1.pdf\n")
    exit()

allC = ["verb", "prep", "prcl", "numr", "npro", "noun", "grnd", "conj", "advb", "adjf"]
selected = "numr"


fileText = sys.argv[1]
db = SQL(fileText+'.frequency_dict.db')
print("Calculating abs for ЧС_частмови...")
dataMany = db.fetch("SELECT * from ЧС_частмови", (), True)
for data in dataMany:
    data = list(data)
    tableNameABS = data[0]
    data.pop(0)
    data.pop(0)
    dataUniq = sorted(set(data))
    sumNi = 0
    sumXiNi = 0
    finishData = {}
    
    db.createTable(f"abs_{tableNameABS}", [
        {"name": "Xi", "params": "INTEGER"},
        {"name": "Ni", "params": "INTEGER"},
        {"name": "XiNi", "params": "INTEGER"}
    ])

    for num in dataUniq:
        finishData[num] = 0
        for num2 in data:
            if num == num2:
                finishData[num] = finishData[num]+1

    for key in finishData:
        val = finishData[key]
        xini = key*val
        sumXiNi = sumXiNi + xini
        sumNi = sumNi + val
        db.executeSql(f"INSERT INTO abs_{tableNameABS} (Xi, Ni, XiNi) VALUES (?, ?, ?)", [key, val, xini])

    print(f"Частина мови: {tableNameABS}")
    print(f"sum ni = {sumNi}")
    print(f"sum xini = {sumXiNi}")

    db.executeSql(f"INSERT INTO abs_{tableNameABS} (Ni, XiNi) VALUES (?, ?)", [sumNi, sumXiNi])
    
    midFreq = sumXiNi/sumNi

    print(f"midFreq = {midFreq}")

    print(f"{tableNameABS} division = {midFreq}")


def findNiSum(first, second, data):
    sumData = 0
    for (xi, ni, xini) in data:
        if xi >= first and xi <= second:
            sumData = sumData+ni
    return sumData
        

with PdfPages('result.'+fileText+'.pdf') as pdf:
    for chast in allC:
        data = db.fetch(f"SELECT * from abs_{chast}", (), True)
        data.pop()
        xiPoints = []
        niPoints = []
        maxXi = 0
        minXi = float("inf")
        for (xi, ni, xini) in data:
            if xi > maxXi:
                maxXi = xi
            if xi < minXi:
                minXi = xi
            xiPoints.append(xi)
            niPoints.append(ni)
        
        r = maxXi - minXi
        k = 5
        h = r/k
        startH = 0

        print(f"Частина мови: {chast}")
        print(f"R = {maxXi} - {minXi} = {r}")
        print(f"k = {k}")
        print(f"h = {r} / {k} = {h}")


        if chast == selected:
            db.createTable(f"inter_var", [
                {"name": "inter", "params": "TEXT"},
                {"name": "ni", "params": "INTEGER"},
                {"name": "mid", "params": "FLOAT"}
            ])
            niSumPoints = []
            midPoints = []

            while(True):
                if(startH >= r):
                    break
                startH = round(startH + h, 1)
                inter = f"{round(startH-h, 1)}-{startH}"
                mid = round(round(startH-h, 1)+round(h/2, 1), 1)
                sumInter = findNiSum(round(startH-h, 1), startH, data)
                midPoints.append(mid)
                niSumPoints.append(float(sumInter))
                db.executeSql(f"INSERT INTO inter_var (inter, ni, mid) VALUES (?, ?, ?)", [inter, sumInter, mid])

            with PdfPages('result2.'+fileText+'.pdf') as pdf2:
                xpoints = np.array(midPoints)
                ypoints = np.array(niSumPoints)
                fig, ax = plt.subplots()
                plt.plot(xpoints, ypoints)
                plt.xlabel("Середина інтервалу")
                plt.ylabel("Ni")
                ax.set_title("Полігон частот")
                pdf2.savefig(fig)  # saves the current figure into a pdf page
                plt.close()

        xpoints = np.array(xiPoints)
        ypoints = np.array(niPoints)
        fig, ax = plt.subplots()
        plt.plot(xpoints, ypoints)
        plt.xlabel("Xi")
        plt.ylabel("Ni")
        ax.set_title(chast)
        pdf.savefig(fig)  # saves the current figure into a pdf page
        plt.close()
