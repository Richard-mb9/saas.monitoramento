import asyncio
from asyncio import wait_for, Future
from typing import Dict, Any, Optional, List
from playwright.async_api import (
    async_playwright,
    Response,
    Browser,
    Page,
    Locator,
    TimeoutError as PlaywrightTimeoutError,
)
from playwright_stealth import Stealth  # type: ignore

from application.interfaces import MonitorInterface
from shared import logger

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
            # context_status = await page.evaluate("navigator.webdriver")

            base_url = "https://cnetmobile.estaleiro.serpro.gov.br"
            url_params = f"?compra={numero_compra}"
            url = f"{base_url}/comprasnet-web/public/compras/acompanhamento-compra{url_params}"

            await self.__acess_page(page=page, url=url)
            logger.info("Fim da listagem")
            resultado = await wait_for(self._future_response, timeout=10)
            return resultado

    async def close(self):
        if self.browser is not None:
            await self.browser.close()
        logger.info("browser finalizado")

    async def __acess_page(self, url: str, page: Page):
        try:
            logger.info("navegando para url: %s", url)
            await page.goto(url)
            await page.wait_for_timeout(3000)
            logger.info("listando mensagens")
            element: Locator = (
                page.get_by_label("Mensagens da compra").filter(visible=True).first
            )

            await element.wait_for(state="visible", timeout=3000)
            await element.click()
            await page.wait_for_timeout(3000)
        except PlaywrightTimeoutError as error:
            logger.error("Houve um erro para carregar todos os dados da pagina")
            if self._future_response and not self._future_response.done():
                self._future_response.set_exception(error)
        except Exception as error:
            logger.error(error)
        finally:
            await self.close()

    async def __on_response(self, response: Response):
        if URL_MENSAGENS in response.url and response.status == 206:
            if self._future_response and not self._future_response.done():
                try:
                    data = await response.json()
                    self._future_response.set_result(data)
                except Exception as e:
                    logger.error("Erro ao parsear JSON: %s", e)
                    self._future_response.set_exception(e)
