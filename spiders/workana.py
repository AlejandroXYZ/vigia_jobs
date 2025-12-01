from dataclasses import dataclass
import spider_base

@dataclass
class Workana(spider_base.Dinamica):

    async def extraer(self,page):
        await page.goto(self.url,timeout=60000)
        await page.wait_for_selector("div.project-item.js-project",timeout=60000)
        busqueda = await page.query_selector_all("div.project-item.js-project h2")
        informacion = await page.query_selector_all("div.project-item.js-project div.html-desc.project-details p")
        enlaces = await page.locator("div.project-item.js-project h2 a").evaluate_all("list_of_a_elements => list_of_a_elements.map(element => element.href)")
        #hora = await page.query_selector_all("div.project-header span.date.visible-xs")
        print("Mostrando Resultados encontrados")
        for i,x,z in zip(busqueda,informacion,enlaces):
            print("=" * 20)
            if await i.inner_text() == "Envía una propuesta":
                continue
            else:
               titulo2= await i.inner_text()
            #print(await h.inner_text())
            informacion = await x.inner_text()
            await self.db(titulo2,z,informacion)
