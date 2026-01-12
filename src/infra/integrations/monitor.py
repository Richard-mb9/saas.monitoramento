import asyncio
from asyncio import wait_for, Future
from typing import Dict, Any, Optional, List
from playwright.async_api import async_playwright, Response, Browser, Page, Locator
from playwright_stealth import Stealth  # type: ignore

from application.interfaces import MonitorInterface

URL_MENSAGENS = "https://cnetmobile.estaleiro.serpro.gov.br/comprasnet-mensagem/v2/chat"


class Monitor(MonitorInterface):
    def __init__(self) -> None:
        self.browser: Optional[Browser] = None
        self._future_response: Optional[Future[Any]] = None

    async def get_messages(self, numero_compra: str) -> List[Dict[str, Any]]:
        self._future_response = asyncio.get_event_loop().create_future()
        async with Stealth().use_async(async_playwright()) as p:
            browser = await p.chromium.launch(headless=False)
            self.browser = browser
            context = await browser.new_context()
            page = await context.new_page()
            page.on("response", self.__on_response)
            context_status = await page.evaluate("navigator.webdriver")
            print(f"status da compra {numero_compra}: {context_status}")

            base_url = "https://cnetmobile.estaleiro.serpro.gov.br"
            url_params = f"?compra={numero_compra}"
            url = f"{base_url}/comprasnet-web/public/compras/acompanhamento-compra{url_params}"

            await self.__acess_page(page=page, url=url)
            print("Fim da listagem")
            resultado = await wait_for(self._future_response, timeout=20)
            return resultado

    async def close(self):
        if self.browser is not None:
            await self.browser.close()
        print("browser finalizado")

    async def __acess_page(self, url: str, page: Page):
        try:
            print(f"navegando para url: {url}")
            await page.goto(url)
            await page.wait_for_timeout(2000)
            print("listando mensagens")
            element: Locator = (
                page.get_by_label("Mensagens da compra").filter(visible=True).first
            )

            await element.click()
            await page.wait_for_timeout(2000)
        except Exception as error:
            print(error)
        finally:
            await self.close()

    async def __on_response(self, response: Response):
        if URL_MENSAGENS in response.url and response.status == 206:
            if self._future_response and not self._future_response.done():
                try:
                    data = await response.json()
                    self._future_response.set_result(data)
                except Exception as e:
                    print(f"Erro ao parsear JSON: {e}")
                    self._future_response.set_exception(e)
