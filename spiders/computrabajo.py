from dataclasses import dataclass
import spider_base
import asyncio

@dataclass
class Computrabajo(spider_base.Dinamica):
    async def extraer(self,page):
        await page.goto(self.url)
        await asyncio.sleep(4)
        datos = await page.evaluate("""
            ()=>{
                const dato = document.querySelectorAll("a.js-o-link.fc_base");
                const url = document.querySelectorAll("a.js-o-link.fc_base");
                lista = [];
                urls = []
                dato.forEach(i=>{
                    lista.push(i.innerText);
                });
                url.forEach(i=>{
                    urls.push(i.href)
                })
                return {dato:lista,url:urls};
            };
        """)
        print("="*30+"Empleos Computrabajo"+"="*30)
        for i,x in zip(datos["dato"],datos["url"]):
            await self.db(i,x,None)
