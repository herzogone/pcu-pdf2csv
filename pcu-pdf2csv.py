# People's Credit (Rhode Island, USA) PDF to CSV statement converter
# Copyright (C) 2024 Brian Clayton (brianpclayton@gmail.com)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys
import pdfplumber
import re
from datetime import datetime
from pathlib import Path

def writeCsvLine():
    csvFile.write(lineDate.strftime("\"%m/%d/%Y") + qcq + description + qcq + wOrD + qcq + balance + "\"\n")
    
qcq = "\",\""
currencyPattern = r"^\-?\d{1,3}(,\d{3})*(\.\d{2})$"
twoDigits = r"^\d{2}$"

print("Copyright (C) 2024 Brian Clayton (brianpclayton@gmail.com)")
print("This program comes with ABSOLUTELY NO WARRANTY; for details see LICENSE")
print("included with this program or go to https://www.gnu.org/licenses\n")

n = len(sys.argv)
if n > 1:
    pdfFilename = sys.argv[1]
    csvFilename = f"{Path(pdfFilename).stem}.csv"
    year = re.search(r"\d{4}", pdfFilename).group()
    with open(csvFilename, "w") as csvFile:
        with pdfplumber.open(pdfFilename) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                foundBalanceLine = False
                descriptionLineCount = 0
                for line in text.split("\n"):
                    isBalanceLine = False
                    cols = line.split()
                    if len(cols) > 4:
                        if len(cols[0]) == 3 and re.search(twoDigits, cols[1]) and re.search(currencyPattern, cols[-1]) and re.search(currencyPattern, cols[-2]):
                            # Write previous balance line, need lookahead for descriptions that span multiple lines
                            if foundBalanceLine:
                                writeCsvLine()
                            foundBalanceLine = True
                            isBalanceLine = True
                            descriptionLineCount = 0
                            lineDate = datetime.strptime(f"{cols[0]} {cols[1]} {year}", "%b %d %Y")
                            description = " ".join(cols[2:-2])
                            wOrD = cols[-2]
                            if wOrD[0] == '-':
                                wOrD += qcq
                            else:
                                wOrD = qcq + wOrD
                            balance = cols[-1]
                    if foundBalanceLine and not isBalanceLine:
                        lineLower = line.lower()
                        # "Ending Balance" or "Date Balance" marks end of table (start of summary), "NOPRT.D.N" is sometimes page footer
                        if "ending balance" in lineLower or "date balance" in lineLower or "noprt.d.n." in lineLower:
                            writeCsvLine()
                            foundBalanceLine = False
                            break
                        # Max 5 lines of additional description
                        if descriptionLineCount > 4:
                            print("Description exceeded expected length, please check results.")
                            break
                        description += " " + line
                        descriptionLineCount += 1

                if foundBalanceLine:
                    writeCsvLine()
    print(f"Wrote {csvFilename}")
else:
    print(f"Usage: {sys.argv[0]} filename.pdf")
    print("\twhere filename.pdf is the name of the PDF-format statement file")
    print("\tto be converted to filename.csv")
