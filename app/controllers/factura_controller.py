from flask import request, redirect, render_template
from app.services.facturacion_service import cerrar_comanda_y_facturar
from app.models.comanda_model import Comanda


def cerrar_comanda(id_comanda):
    if request.method == 'POST':
        metodo_pago = request.form['metodo_pago']

        ok, resultado = cerrar_comanda_y_facturar(id_comanda, metodo_pago)

        if not ok:
            return f"Error: {resultado}"

        return redirect(f'/factura/{resultado}')

    return render_template('factura/cerrar.html', id_comanda=id_comanda)


def ver_factura(id_factura):
    from app.models.factura_model import Factura
    factura = Factura.query.get(id_factura)

    return render_template('factura/ver.html', factura=factura)