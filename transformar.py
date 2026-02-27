import csv
import re

input_file = 'ProductosActuales.csv'
output_file = 'productos_para_medusa_final.csv'

def make_url_safe(handle):
    """Convierte un string en un handle válido para URL (solo letras, números y guiones)."""
    safe = handle.replace('_', '-')
    safe = re.sub(r'[^a-zA-Z0-9-]', '', safe)
    return safe.lower()

# Encabezados exactos del template de importación de Medusa
fieldnames_dest = [
    'Product Id',
    'Product Handle',
    'Product Title',
    'Product Subtitle',
    'Product Description',
    'Product Status',
    'Product Thumbnail',
    'Product Weight',
    'Product Length',
    'Product Width',
    'Product Height',
    'Product HS Code',
    'Product Origin Country',
    'Product MID Code',
    'Product Material',
    'Shipping Profile Id',
    'Product Sales Channel 1',
    'Product Collection Id',
    'Product Type Id',
    'Product Tag 1',
    'Product Discountable',
    'Product External Id',
    'Variant Id',
    'Variant Title',
    'Variant SKU',
    'Variant Barcode',
    'Variant Allow Backorder',
    'Variant Manage Inventory',
    'Variant Weight',
    'Variant Length',
    'Variant Width',
    'Variant Height',
    'Variant HS Code',
    'Variant Origin Country',
    'Variant MID Code',
    'Variant Material',
    'Variant Price EUR',
    'Variant Price USD',
    'Variant Option 1 Name',
    'Variant Option 1 Value',
    'Product Image 1 Url',
    'Product Image 2 Url'
]

with open(input_file, mode='r', encoding='utf-8-sig') as infile, \
     open(output_file, mode='w', encoding='utf-8-sig', newline='') as outfile:

    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=fieldnames_dest)
    writer.writeheader()

    for i, row in enumerate(reader, start=1):
        original_id = row.get('handleId', '').strip()
        if not original_id:
            print(f"⚠️  Fila {i}: 'handleId' vacío, se omite.")
            continue

        # Generar handle: parfum + ID seguro
        safe_id = make_url_safe(original_id)
        product_handle = f"parfum-{safe_id}"

        # Extraer otros campos
        name = row.get('name', '').strip()
        sku = row.get('sku', '').strip()
        field_type = row.get('fieldType', '').strip()
        description = row.get('description', '').strip()
        visible = row.get('visible', 'false').strip().lower() == 'true'
        product_status = 'published' if visible else 'draft'
        product_image_url = row.get('productImageUrl', '').strip()
        weight = row.get('weight', '').strip()
        brand = row.get('brand', '').strip()
        price = row.get('price', '').strip()

        dest_row = {
            'Product Id': '',
            'Product Handle': product_handle,
            'Product Title': name,
            'Product Subtitle': field_type,
            'Product Description': description,
            'Product Status': product_status,
            'Product Thumbnail': product_image_url,
            'Product Weight': weight,
            'Product Length': '',
            'Product Width': '',
            'Product Height': '',
            'Product HS Code': '',
            'Product Origin Country': '',
            'Product MID Code': '',
            'Product Material': '',
            'Shipping Profile Id': '',
            'Product Sales Channel 1': '',               # ← VACÍO para evitar errores
            'Product Collection Id': '',
            'Product Type Id': '',
            'Product Tag 1': brand,
            'Product Discountable': 'true',
            'Product External Id': original_id,
            'Variant Id': '',
            'Variant Title': 'Default variant',
            'Variant SKU': sku,
            'Variant Barcode': '',
            'Variant Allow Backorder': 'false',
            'Variant Manage Inventory': 'true',
            'Variant Weight': weight,
            'Variant Length': '',
            'Variant Width': '',
            'Variant Height': '',
            'Variant HS Code': '',
            'Variant Origin Country': '',
            'Variant MID Code': '',
            'Variant Material': '',
            'Variant Price EUR': price,
            'Variant Price USD': price,
            'Variant Option 1 Name': 'Default option',
            'Variant Option 1 Value': 'Default',
            'Product Image 1 Url': product_image_url,
            'Product Image 2 Url': ''
        }

        writer.writerow(dest_row)

print(f"✅ Archivo generado: {output_file}")