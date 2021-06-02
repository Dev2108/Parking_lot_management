from __future__ import absolute_import, unicode_literals

from celery import  shared_task

@shared_task
def add():
    return 4 + 7

# def data_to_xlsx(speakers):

#     wb=Workbook()
#         # grab the active worksheet
#     ws = wb.active
#         # Data can be assigned directly to cells
#     ws['A1'].fill = PatternFill(start_color="0000CCFF", fill_type = "solid")
#     ws['A1'] = 'vehicle_no'
#     ws['B1'].fill = PatternFill(start_color="0000CCFF", fill_type = "solid")
#     ws['B1'] = 'entry_time'
#     ws['c1'].fill = PatternFill(start_color="0000CCFF", fill_type = "solid")
#     ws['C1'] = 'exit_time'
#     ws['D1'].fill = PatternFill(start_color="0000CCFF", fill_type = "solid")
#     ws['D1'] = 'Ratings'
#     ws['E1'].fill = PatternFill(start_color="0000CCFF", fill_type = "solid")
#     ws['E1'] = 'cost'
#     for i in speakers:
        
#         ws.append(i)
        
#     # Save the file
#     wb.save("parking.xlsx")
#     return 0
    