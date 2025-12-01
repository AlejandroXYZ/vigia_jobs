from dataclasses import dataclass
import spider_base

class Linkedin(spider_base.Estatica):
    async def extraer(self,soup):
        a = soup.select("h3.base-search-card__title")
        url = soup.select("a.base-card__full-link")
        location = soup.select("span.job-search-card__location")
        print("="*20+"Linkedin Jobs"+ "=" * 20)
        for i,l,url in zip(a,location,url):
            titulo = (i.text).strip()
            ubicacion = l.text.strip()
            url = url['href']
            await self.db(titulo,url,None)
