## Enunciado
# Debes construir una API para gestionar una aplicación de tareas (to-do list).
# La API debe permitir la creación, lectura, actualización y eliminación de tareas.
# Además, deberá incluir funcionalidades adicionales como la asignación de etiquetas a las tareas, la marcación de tareas como completadas,
# y la posibilidad de filtrar tareas según diferentes criterios.
## Requerimientos Funcionales
# Crear Tarea: Debe ser posible agregar una nueva tarea con un título, descripción y opcionalmente una fecha de vencimiento. La descripcion no puede tener mas de 120 caracteres.✅
# Listar Tareas: La API debe proporcionar un endpoint para obtener la lista de todas las tareas, permitir filtro por estado ✅
# Actualizar Tarea: Debe ser posible actualizar el estado (completada o pendiente), la descripción o la fecha de vencimiento de una tarea existente.✅
# Eliminar Tarea: La API debe permitir la eliminación de una tarea por su id.✅
# Etiquetas: Implementar la capacidad de agregar etiquetas a las tareas y permitir filtrar las tareas por estas etiquetas.✅
# Marcación de Tareas Completadas: Permitir marcar una tarea como completada.✅
## Requerimientos Técnicos
# Utilizar FastAPI (ultima version) para construir la API.✅
# Utilizar Pydantic (ultima version) para la validación de datos.✅
# Utilizar un sistema de almacenamiento en memoria para las tareas (puedes utilizar una lista o diccionario).✅
# Implementar manejo de errores y retornar respuestas HTTP apropiadas.✅
## Puntos Extras (Opcionales)
# - Tener un sistema de “proteccion” para los endpoints, en el cual se debe enviar obligatoriamente el `header` `X-movitronics` con el valor “movietronics_secret_api_key” ->
# esto es muy parecido a si tuvieramos que autenticarnos con API_KEYs para poder interactuar con nuestro backend✅
# - Permitir filtrar por fecha de vencimiento, y etiquetas.✅
# - Usar SQLite o MongoDB (con docker) en vez de una lista/diccionario en memoria✅
## Se valorará mucho los siguientes puntos
# - La estructura utilizada a la hora de armar la API debe ser modular y generalizada. Por ej, suponiendo que en un futuro se quisieran agregar usuarios y proyectos,
# deberia ser intuitivo saber por donde empezar para hacer este tipo de actualizaciones✅
# - Buenas practicas: usar bien los features de FastAPI (Body, Query, Header, Depends). Nombrar bien las variables, funciones, endpoints, usar los verbos correctos, etc✅


from fastapi import FastAPI
from app.routes.todo_route import router as todo_router
from app.models.todo_model import Base
from app.database.database import engine


Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(todo_router)
