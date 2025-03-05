from datetime import datetime
from matplotlib import pyplot as plt
from config import COLUMNS
from database import get_data
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT


def generate_daily_sales_report(date : datetime) -> bool:

    '''
    Fetching all the sales data for date and storing as a DataFrame
    '''

    data  = pd.DataFrame(get_data(date), columns= COLUMNS) 

    '''
    Calculating the total orders for date
    '''
    
    total_orders = len(data['order_number'].unique())
    total_articles = len(data['article'])

    '''
    Grouping data and getting the total sold for each article
    '''

    gdata = data[['article','quantity','unit_price']].copy()
    grouped_data = gdata.groupby('article', as_index=False).sum() 
    
    '''
    Creating a Bar graph to visualize sales with respect to each article
    '''
    
    plt.bar(grouped_data['article'],grouped_data['quantity'])
    plt.title('Daily Bakery Sales')
    plt.xlabel('Articles')
    plt.ylabel('Quantity')
    plt.xticks(rotation=45, ha="right")  # Align text to the right
    plt.tight_layout()
    salesimg = "sales.png"
    plt.savefig(salesimg)

    '''
    Calculating the total revenue for the day
    '''

    grouped_data['revenue_for_articles'] = grouped_data['quantity'] * grouped_data['unit_price']
    revenue = grouped_data['revenue_for_articles'].sum(axis=0)

    '''
    Creating the actual pdf. The pdf needs more beautification
    '''
    styles = getSampleStyleSheet()
    
    style_heading = ParagraphStyle(
        "CustomHeading",
        parent=styles["Heading1"],  
        fontName="Helvetica-Bold",
        fontSize=16,
        alignment=TA_CENTER,
        spaceBefore=0,
        spaceAfter=20,
        leading=20
    )

    style_text = ParagraphStyle(
        "CustomNormal",
        parent=styles["Normal"],  
        fontName="Times-Roman",  
        fontSize=12,              
        textColor=colors.black,   
        alignment=TA_LEFT,        
        leading=14,               
        spaceBefore=5,            
        spaceAfter=20
    )

    try:

        story = []

        story.append(Paragraph(f"Daily Sales Report {date: %Y-%m-%d}",style_heading))
        story.append(Paragraph(f"""On {date: %B %d, %Y}, our bakery processed a total of {total_orders} orders, generating a revenue of € {revenue}. 
                            Throughout the day, a total of {total_articles} items were sold.
                            By analyzing these figures, we can refine our inventory and pricing strategies to enhance profitability and 
                            reduce waste while meeting customer demand efficiently.""",
            style_text))
        
        #creating Table
        table_data = [COLUMNS]
        table_data += [col[1:] for col in data.reset_index().values.tolist()]

        row_height = len(table_data)*[30]
        col_widths = [30] + 3 * [75] + [130] + 2 * [75]

        #create and style the table
        table = Table(table_data, colWidths=col_widths, rowHeights= row_height, repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
            ("BACKGROUND", (0, 1), (-1, -1), colors.lightgoldenrodyellow),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(table)
        PAGE_WIDTH, PAGE_HEIGHT = letter
        img = Image("sales.png", width=PAGE_WIDTH - 150, height=PAGE_HEIGHT / 2)  # Leaving some margins
        story.append(img)
        doc = SimpleDocTemplate(f'reports/Sales Report {date: %Y-%m-%d}.pdf',pagesize = letter)
        doc.build(story)
        
        return True
    except Exception as e:
        print(e)
        return False