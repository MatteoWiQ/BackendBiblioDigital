from database import SessionLocal, engine
import models
from security import get_password_hash

def poblar_base_de_datos():
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        print("Iniciando la inserción de datos de prueba...")


        admins = [
            {"email": "ana.admin@biblioteca.com", "password": "adminpassword1", "rol": "Admin"},
            {"email": "carlos.admin@biblioteca.com", "password": "adminpassword2", "rol": "Admin"}
        ]
        
        for adv in admins:

            existe = db.query(models.User).filter(models.User.email == adv["email"]).first()
            if not existe:
                nuevo_admin = models.User(
                    email=adv["email"],
                    hashed_password=get_password_hash(adv["password"]), # Usamos tu nueva función segura de bcrypt
                    rol=adv["rol"]
                )
                db.add(nuevo_admin)
                print(f"-> Administrador creado: {adv['email']}")

        usuarios = [
            {"email": "juan.perez@correo.com", "password": "user123", "rol": "Usuario"},
            {"email": "maria.gomez@correo.com", "password": "user123", "rol": "Usuario"},
            {"email": "luis.torres@correo.com", "password": "user123", "rol": "Usuario"},
            {"email": "ana.lopez@correo.com", "password": "user123", "rol": "Usuario"},
            {"email": "diego.sanchez@correo.com", "password": "user123", "rol": "Usuario"}
        ]

        for usr in usuarios:
            existe = db.query(models.User).filter(models.User.email == usr["email"]).first()
            if not existe:
                nuevo_usuario = models.User(
                    email=usr["email"],
                    hashed_password=get_password_hash(usr["password"]),
                    rol=usr["rol"]
                )
                db.add(nuevo_usuario)
                print(f"-> Usuario normal creado: {usr['email']}")


        libros = [
            {
                "titulo": "Cien años de soledad",
                "autor": "Gabriel García Márquez",
                "descripcion": "La obra cumbre del realismo mágico que narra la historia de la familia Buendía en Macondo.",
                "url_pdf": "https://www.cultura.gob.ar/archivos/libros/cien-anos-soledad.pdf",
                "categoria": "Novela",
                "precio": 120.50
            },
            {
                "titulo": "Don Quijote de la Mancha",
                "autor": "Miguel de Cervantes",
                "descripcion": "Las divertidas y trágicas aventuras de un hidalgo que perdió la cabeza por leer libros de caballería.",
                "url_pdf": "http://www.bne.es/quijote/Quijote_Parte1.pdf",
                "categoria": "Clásico",
                "precio": 150.00
            },
            {
                "titulo": "El principito",
                "autor": "Antoine de Saint-Exupéry",
                "descripcion": "Una hermosa fábula infantil que aborda temas profundos como el amor, la amistad y el sentido de la vida.",
                "url_pdf": "https://biblioteca.org.ar/libros/el-principito.pdf",
                "categoria": "Infantil",
                "precio": 80.00
            },
            {
                "titulo": "1984",
                "autor": "George Orwell",
                "descripcion": "Una perturbadora novela distópica sobre el control absoluto del Gran Hermano y la pérdida de la privacidad.",
                "url_pdf": "https://www.marxists.org/espanol/orwell/1984.pdf",
                "categoria": "Ciencia Ficción",
                "precio": 110.00
            },
            {
                "titulo": "Crónica de una muerte anunciada",
                "autor": "Gabriel García Márquez",
                "descripcion": "Una novela corta donde se relata con detalles el asesinato programado de Santiago Nasar.",
                "url_pdf": "https://www.literatura.us/garciamarquez/cronica.pdf",
                "categoria": "Novela",
                "precio": 95.50
            },
            {
                "titulo": "Ficciones",
                "autor": "Jorge Luis Borges",
                "descripcion": "Una genial colección de cuentos e historias laberínticas repletas de filosofía, espejos y acertijos intelectuales.",
                "url_pdf": "https://borgestodoelanio.blogspot.com/ficciones.pdf",
                "categoria": "Cuentos",
                "precio": 130.00
            },
            {
                "titulo": "Pedro Páramo",
                "autor": "Juan Rulfo",
                "descripcion": "Juan Preciado viaja al pueblo fantasma de Comala para buscar a su padre, un terrateniente llamado Pedro Páramo.",
                "url_pdf": "http://www.descargascultura.unam.mx/pedro-paramo.pdf",
                "categoria": "Realismo Mágico",
                "precio": 100.00
            },
            {
                "titulo": "Rayuela",
                "autor": "Julio Cortázar",
                "descripcion": "Una contranovela revolucionaria que se puede leer en diferentes órdenes, siguiendo la vida de Horacio Oliveira.",
                "url_pdf": "https://www.unlp.edu.ar/rayuela-cortazar.pdf",
                "categoria": "Novela",
                "precio": 145.00
            },
            {
                "titulo": "El Alquimista",
                "autor": "Paulo Coelho",
                "descripcion": "La inspiradora historia de Santiago, un joven pastor andaluz que emprende un viaje en busca de su leyenda personal.",
                "url_pdf": "https://www.coelho-alquimista.com/libro.pdf",
                "categoria": "Autoayuda / Ficción",
                "precio": 90.00
            },
            {
                "titulo": "La metamorfosis",
                "autor": "Franz Kafka",
                "descripcion": "El impactante relato de Gregorio Samsa, un comerciante que amanece un día transformado en un monstruoso insecto.",
                "url_pdf": "https://www.elejandria.com/libro/la-metamorfosis/kafka-franz.pdf",
                "categoria": "Clásico",
                "precio": 85.00
            }
        ]

        for lib in libros:
            
            existe = db.query(models.Book).filter(models.Book.titulo == lib["titulo"]).first()
            if not existe:
                nuevo_libro = models.Book(
                    titulo=lib["titulo"],
                    autor=lib["autor"],
                    descripcion=lib["descripcion"],
                    url_pdf=lib["url_pdf"],
                    categoria=lib["categoria"], 
                    precio=lib["precio"]        
                )
                db.add(nuevo_libro)
                print(f"-> Libro insertado: '{lib['titulo']}' a Bs {lib['precio']}")
        
        db.commit()
        print("\n¡ÉXITO TOTAL! Todos los datos de prueba han sido inyectados con éxito en la base de datos.")

    except Exception as e:
        db.rollback()
        print(f"\n[ERROR] Ocurrió un problema al insertar los datos: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    poblar_base_de_datos()