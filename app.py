import io
import pandas as pd
import streamlit as st

st.set_page_config(page_title='SellerOps Accountant | Web Trial',layout='wide')
st.title('SellerOps / MANZEL — Accountant Web Trial')
st.warning('واجهة تجريبية مستقلة. ليست نقلًا مثبتًا لمحرك CP15، ولا معتمدة للإقفال المالي. CP15 / Master Register v1.14 هو المرجع المعتمد.')
st.caption('لا ترفع بيانات حقيقية إلى استضافة عامة قبل اعتماد سياسة الخصوصية والصلاحيات.')

def load_amazon_csv(data):
    raw=data.decode('utf-8-sig',errors='replace')
    lines=raw.splitlines()
    idx=next((i for i,line in enumerate(lines) if line.lower().startswith('"date/time"') or line.lower().startswith('date/time,')),None)
    if idx is None: raise ValueError('لم يتم العثور على صف عناوين Amazon Transaction')
    return pd.read_csv(io.StringIO('\n'.join(lines[idx:])),low_memory=False)

files=st.file_uploader('ارفع Amazon Transaction CSV (يمكن اختيار عدة ملفات)',type=['csv'],accept_multiple_files=True)
if files:
    tables=[]
    for f in files:
        try:
            df=load_amazon_csv(f.getvalue()); df.insert(0,'source_file',f.name);tables.append(df)
            st.success(f'{f.name}: {len(df):,} صف')
        except Exception as e: st.error(f'{f.name}: {e}')
    if tables:
        data=pd.concat(tables,ignore_index=True)
        a,b,c=st.columns(3)
        a.metric('الصفوف المحمّلة',f'{len(data):,}')
        b.metric('Refund (حسب Type)',f'{data["type"].astype(str).str.lower().eq("refund").sum():,}' if 'type' in data else 'غير متاح')
        c.metric('ملفات محمّلة',len(tables))
        st.subheader('توزيع أنواع الحركات — فحص وصفي فقط')
        if 'type' in data: st.dataframe(data['type'].fillna('(missing)').value_counts().rename_axis('Type').reset_index(name='Rows'),use_container_width=True)
        st.subheader('معاينة الحركات')
        st.dataframe(data.head(300),use_container_width=True)
        st.download_button('تنزيل بيانات المعاينة CSV',data.head(300).to_csv(index=False).encode('utf-8-sig'),'sellerops_preview.csv','text/csv')
        st.info('لا تُحسب هنا أرصدة أو أرباح أو COGS أو استحقاقات Refund. دمج المحرك المالي المعتمد مؤجل لحين إتاحة كود CP15 الأصلي.')
else:
    st.info('ابدأ بملف CSV تجريبي. لن تُنفّذ أي عملية مالية قبل تحميل البيانات.')
