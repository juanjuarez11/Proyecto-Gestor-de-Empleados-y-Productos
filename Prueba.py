
def obtener_detalles(detalle, ventas):
    for venta in ventas:
        for c,v in venta.items():
            if c == 'detalle':
                for subdict in v:
                    return subdict[detalle]
def obtener_detalle(detalle, factura):
    
    for c,v in factura.items():
        if c == 'detalle':
            for subdict in v:
                return subdict[detalle]