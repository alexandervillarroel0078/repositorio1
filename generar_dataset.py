from faker import Faker
import pandas as pd

fake = Faker()

# Generamos datos para 100 estudiantes
data = []
for _ in range(100):  # Puedes cambiar el número de estudiantes si lo necesitas
    data.append({
        'alumno_id': fake.unique.random_int(min=1, max=1000),  # ID único para cada estudiante
        'nombre_completo': fake.name(),
        'email': fake.email(),
        'telefono': fake.phone_number(),
        'direccion': fake.address(),
        'fecha_nacimiento': fake.date_of_birth(),
        'estado': fake.random_element(elements=('activo', 'inactivo')),
        'grado': fake.random_int(min=1, max=6),  # Grados de 1 a 6
        'nota': fake.random_int(min=1, max=10)  # Puedes ajustar las notas si lo necesitas
    })

# Crear el DataFrame
df = pd.DataFrame(data)

# Guardar el DataFrame en un archivo CSV
df.to_csv('dataset_estudiantes.csv', index=False)

print("Dataset generado y guardado en 'dataset_estudiantes.csv'")
