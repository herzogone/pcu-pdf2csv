# pcu-pdf2csv
People's Credit Union (Rhode Island, USA) PDF to CSV statement converter
Copyright (C) 2024 [Brian Clayton](mailto:brianpclayton@gmail.com?subject=pcu-pdf2csv)

This program comes with ABSOLUTELY NO WARRANTY; 
This is free software, and you are welcome to redistribute it under certain conditions;
See LICENSE for details.

## Requirements
[Python](https://www.python.org/) is required. This was initially developed and tested with 
[Python 3.12.3](https://www.python.org/downloads/release/python-3123/).

The excellent [pdfplumber](https://github.com/jsvine/pdfplumber) module is also required.
It does all the hard work of parsing PDF format; much thanks to all who contribute!

## Overview
This was originally developed for the author's personal use to enable import into other
software for managing finances. It is shared in hopes others might benefit.

The output CSV format consists of the five basic columns from the statement PDF:
Date, Transaction Description, Withdrawal, Deposit, and Balance

Column headers are omitted for brevity and ease of copy/paste.
