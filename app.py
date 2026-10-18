import io
import json
import pandas as pd
import streamlit as st

st.set_page_config(page_title='SellerOps Accountant | Web Trial v0.2', layout='wide')
st.title('SellerOps / MANZEL — Accountant Web Trial v0.2')
st.warning('نسخة فحص بيانات تجريبية مستقلة؛ ليست محرك CP15 ولا تصلح للإقفال المالي. CP15 / Master Register v1.14 هو المرجع المعتمد.')
st.caption('تنبيه خصوصية: التطبيق مستضاف علنًا. لا ترفع بيانات مالية حقيقية قبل مراجعة ضوابط الوصول والاحتفاظ بالبيانات.')

REQUIRED = ['date/time', 'type', 'order id', 'sku']

def read_amazon_csv(blob):
    raw = blob.decode('utf-8-sig', errors='replace')
    lines = raw.splitlines()
    header = next((i for i, line in enumerate(lines) if line.strip().lower().startswith(('"date/time"', 'date/time,'))), None)
    if header is None:
        raise ValueError('لم يتم العثور على صف عناوين Amazon Transaction')
    df = pd.read_csv(io.StringIO('\n'.join(lines[header:])), dtype=str, keep_default_na=False)
    df.columns = [str(c).strip().lower() for c in df.columns]
    return df

files = st.file_uploader('Amazon Transaction CSV — ملف واحد أو عدة ملفات', type=['csv'], accept_multiple_files=True)
if files:
    tables = []
    errors = []
    for file in files:
        try:
            df = read_amazon_csv(file.getvalue())
            df.insert(0, 'source_file', file.name)
            tables.append(df)
            st.success(f'{file.name}: {len(df):,} صف')
        except Exception as exc:
            errors.append({'file': file.name, 'error': str(exc)})
            st.error(f'{file.name}: {exc}')
    if tables:
        data = pd.concat(tables, ignore_index=True)
        missing = [c for c in REQUIRED if c not in data.columns]
        type_counts = (data['type'].replace('', '(missing)').value_counts(dropna=False) if 'type' in data else pd.Series(dtype='int64'))
        refund_count = int(data['type'].str.strip().str.lower().eq('refund').sum()) if 'type' in data else None
        a, b, c = st.columns(3)
        a.metric('الصفوف المحمّلة', f'{len(data):,}')
        b.metric('Refund (حسب Type)', f'{refund_count:,}' if refund_count is not None else 'غير متاح')
        c.metric('الملفات المقروءة', len(tables))
        st.subheader('فحص جودة البيانات')
        if missing:
            st.error('أعمدة أساسية غير موجودة: ' + ', '.join(missing))
        else:
            st.success('الأعمدة الأساسية متاحة — لا يعني ذلك صحة البيانات ماليًا')
        quality = pd.DataFrame([{'column': col, 'missing_or_blank_rows': int(data[col].astype(str).str.strip().eq('').sum())} for col in REQUIRED if col in data.columns])
        st.dataframe(quality, use_container_width=True, hide_index=True)
        # Exact duplicate content is a review signal only: legitimate Amazon rows may be identical.
        exact_dupes = int(data.drop(columns=['source_file']).duplicated(keep=False).sum())
        st.info(f'صفوف ذات محتوى متطابق محتمل: {exact_dupes:,}. هذه إشارة للمراجعة وليست أمرًا بالحذف أو إثباتًا لخطأ.')
        st.subheader('توزيع أنواع الحركات — فحص وصفي فقط')
        if len(type_counts):
            st.dataframe(type_counts.rename_axis('Type').reset_index(name='Rows'), use_container_width=True, hide_index=True)
        else:
            st.warning('عمود type غير متاح؛ لا يمكن حساب توزيع الحركات')
        st.subheader('معاينة أول 300 صف')
        st.dataframe(data.head(300), use_container_width=True)
        summary = {'trial_version': 'v0.2', 'authority': 'CP15 / Master Register v1.14 (user-approved, not implemented in this trial)', 'rows_loaded': int(len(data)), 'files_loaded': [f.name for f in files if f.name in data['source_file'].unique()], 'refund_rows_by_type': refund_count, 'missing_required_columns': missing, 'exact_content_duplicate_rows_review_only': exact_dupes, 'transaction_type_counts': {str(k): int(v) for k, v in type_counts.items()}, 'file_errors': errors, 'accounting_engine_executed': False}
        st.download_button('تنزيل تقرير فحص البيانات JSON', json.dumps(summary, ensure_ascii=False, indent=2).encode('utf-8'), 'sellerops_data_quality_report.json', 'application/json')
        st.download_button('تنزيل معاينة CSV', data.head(300).to_csv(index=False).encode('utf-8-sig'), 'sellerops_preview.csv', 'text/csv')
        st.caption('لا تُحسب أرباح أو أرصدة أو COGS أو استحقاقات Refund في هذه النسخة.')
else:
    st.info('ابدأ بملف CSV تجريبي منزوع البيانات الحساسة.')
