from app import create_app

app = create_app()

if __name__ == "__main__":
    # Ejecutar en modo debug para ver errores en tiempo real durante el desarrollo
    app.run(debug=True, host='0.0.0.0', port=5000)