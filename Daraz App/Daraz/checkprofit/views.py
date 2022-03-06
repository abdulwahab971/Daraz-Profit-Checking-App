from distutils.command.upload import upload
from hashlib import new
from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
# Create your views here.

import pandas as pd
import numpy as np
import os
from pathlib import Path

url1=[]


def home(request):
    BASE_DIR = Path(__file__).resolve().parent.parent
    dir1 = os.path.join(BASE_DIR,'media')
    print(dir1)
    
    for f in os.listdir(dir1):
        os.remove(os.path.join(dir1, f))
    

    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        file = fs.save(uploaded_file.name, uploaded_file)
        pathdf = fs.path(file)
        pathdf = pathdf.replace("\\", "/")
        url1.insert(0,pathdf)

                
        return redirect('enter_Retail_prices')
    return render(request,'checkprofit/homenew.html')

def enterretailprices(request):
    

    data = pd.read_csv(url1[0])
    grouped_df = data.groupby(['Order No.','Seller SKU'])    
    gb = grouped_df.groups

    orderno=[]
    sku=[]
    retail=[]
    Fee_Name = []
    amount=[]
    Quantity = []
    for values in grouped_df:
        o=values[1]['Order No.'].unique()
        s=values[1]['Seller SKU'].unique()
        a=values[1]['Amount'].sum()
        fitl= (values[1]['Fee Name']=='Item Price Credit' )
        q = values[1]['Fee Name'][fitl].count()

        
        
        #da[o[0]]=[s[0],a]
        orderno.append(o[0])
        sku.append(s[0])
        amount.append(a)
        Quantity.append(q)
        
    da={
        'OrderNo':orderno,
        'SKU':sku,
        'Quantity':Quantity,
        'Daraz Amount':amount,
        
        
    }
    global df
    df= pd.DataFrame(da)

    df['Retail Price'] = np.NaN
    
    uniqueSKU =df['SKU'].unique()
    if request.method == 'POST':
        # print(request.POST.get('clear-tape-2inch-03'))
        for a in uniqueSKU:
            filt = (df['SKU'] == str(a))
            df.loc[filt,['Retail Price']] = df['Quantity'] * float(request.POST.get(a))
            
            
    
        return redirect('display')
        

    context= {
            'uniqueSKU':uniqueSKU

        }    


    return render(request, 'checkprofit/EnterRetailPrices.html',context)




def display(request):
    classes = 'table table-striped table-bordered table-hover table-sm'
    profit = df['Daraz Amount'].sum() - df['Retail Price'].sum()
    html = df.to_html(classes=classes)
    
    context = {
        'html':html,
        'profit':profit

    }
    return render(request,'checkprofit/display.html',context)