import asyncio
import spiders
import spider_base


# Instanciando Arañas

async def main():
      workana = spiders.workana.Workana("Workana","Dinamica","https://www.workana.com/es/jobs?language=es")
      linkedin = spiders.linkedin.Linkedin("Linkedin","Estática","https://ve.linkedin.com/jobs/python-empleos")
      computrabajo = spiders.computrabajo.Computrabajo("Computrabajo","Estatica","https://ve.computrabajo.com/trabajo-de-programador-python")
      arañas = [workana,linkedin,computrabajo]
      for araña in arañas:
         await araña.peticion()


asyncio.run(main())
