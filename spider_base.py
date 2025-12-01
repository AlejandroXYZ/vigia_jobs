from abc import ABC,abstractmethod
from typing import Optional,Any
from dataclasses import dataclass
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as bs
from playwright.async_api import async_playwright
import asyncio
import requests
import sqlite3 as sql
import hashlib
import telegram

# Creando Plantilla base de las arañas

@dataclass
class Araña(ABC):
    nombre: str
    tipo: str
    url: str
    
    @abstractmethod
    def peticion(self):
        pass

    def __post_init__(self):
        self.new_table()

    def new_table(self):
        conn = sql.connect("empleos.db")
        cursor = conn.cursor()
        cursor.execute("""
         CREATE TABLE IF NOT EXISTS Empleos(hash_id TEXT PRIMARY KEY,Titulo TEXT NOT NULL,URL TEXT, Descripcion TEXT, Sitio TEXT);
         """)
        conn.commit()
        cursor.close()
        conn.close()

        
    def generar_hash(self,titulo:str,url:str):
        titulo_limpio = titulo.strip().lower()
        url_limpia = url.split('?')[0].strip()
        hashing = f"{titulo_limpio}{url_limpia}"
        titulo_cod = hashing.encode("utf-8")
        hash_id = hashlib.md5(titulo_cod).hexdigest()
        return hash_id
    

    async def guardar_datos(self,cursor,titulo,url,Descripcion):
        hash_id = self.generar_hash(titulo,url)
        cursor.execute("""
        INSERT OR IGNORE into Empleos(hash_id,Titulo,URL,Descripcion,Sitio) VALUES (?,?,?,?,?);
        """, (hash_id,titulo,url,Descripcion,self.nombre))
        is_new = cursor.rowcount > 0 
        if is_new:
            print(f"[+] Nueva {titulo[:30]}...")
        return is_new 
            

    async def db(self,titulo:str,url:str,Descripcion:Any):
        connection = sql.connect("empleos.db")
        cursor = connection.cursor()
        fue_new = await self.guardar_datos(cursor,titulo,url,Descripcion)
        if fue_new:
            await telegram.sender(titulo,url)
        connection.commit()
        cursor.close()
        connection.close()
        return fue_new
        
@dataclass
class Estatica(Araña):

    async def peticion(self):
        header = {"UserAgent":(UserAgent(platforms="desktop")).random}
        peticion = requests.get(self.url,headers=header)
        soup = bs(peticion.text,"lxml")
        await self.extraer(soup)

    @abstractmethod
    def extraer(self,soup):
        pass


@dataclass
class Dinamica(Araña):

    async def peticion(self):
        async with async_playwright() as p:
            print("Lanzando Navegador")
            browser = await p.firefox.launch(
                headless=False,
                args=["--disable-blink-features=AutomationControlled","--no-sandbox"]
            )
            header = (UserAgent(platforms="desktop")).random
            print("Creando Contexto")
            context = await browser.new_context(user_agent=header)

            await context.add_init_script("""
                Object.defineProperty(navigator,'webdriver',{get:()=> undefined});
            """) 
            print("Creando página")
            page = await context.new_page()
            await self.extraer(page)
            print("Cerrando Navegador")
            await browser.close()
            
    @abstractmethod
    def extraer(self):
        pass
