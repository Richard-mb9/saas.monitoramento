import asyncio
from asyncio import get_event_loop, Future
from json import dumps
from typing import Dict, Any, Optional
from time import sleep
from playwright.async_api import (
    async_playwright,
    Response,
    Browser,
    Page,
    Locator,
    BrowserContext,
)
from playwright_stealth import Stealth

URL_MENSAGENS = "https://cnetmobile.estaleiro.serpro.gov.br/comprasnet-mensagem/v2/chat"


class Monitor:
    def __init__(self) -> None:
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self._future_response: Optional[Future[Any]] = None

    async def start(self):
        """Inicia o browser e a página uma única vez."""
        pw_context = async_playwright()
        Stealth().use_async(pw_context)
        self.playwright = await pw_context.start()
        self.browser = await self.playwright.chromium.launch(headless=False)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()

        # Configura o stealth e o listener global de respostas
        self.page.on("response", self.__on_response)
        print("Browser iniciado e aguardando comandos.")

    async def get_messages(self, numero_compra: str) -> Any:
        """Navega até a compra e retorna o primeiro JSON capturado."""
        if not self.page:
            raise Exception("Browser não iniciado. Chame o método 'start()' primeiro.")

        # Reinicia o Future para esta nova busca
        self._future_response = asyncio.get_event_loop().create_future()

        base_url = "https://cnetmobile.estaleiro.serpro.gov.br"
        url_params = f"?compra={numero_compra}"
        url = f"{base_url}/comprasnet-web/public/compras/acompanhamento-compra{url_params}"

        try:
            print(f"Navegando para compra: {numero_compra}")
            await self.page.goto(url)
            await self.page.wait_for_timeout(2000)  # Pequena pausa para carregar

            # Localiza e clica no elemento de mensagens
            element = (
                self.page.get_by_label("Mensagens da compra").filter(visible=True).first
            )
            await element.click()

            # Aguarda o __on_response preencher o Future (com timeout de 20s)
            print("Aguardando captura do JSON...")
            resultado = await asyncio.wait_for(self._future_response, timeout=20)
            return resultado

        except asyncio.TimeoutError:
            print(f"Timeout: JSON não capturado para a compra {numero_compra}")
            return None
        except Exception as e:
            print(f"Erro durante get_messages: {e}")
            return None

    async def __on_response(self, response: Response):
        if URL_MENSAGENS in response.url and response.status == 206:
            if self._future_response and not self._future_response.done():
                try:
                    data = await response.json()
                    self._future_response.set_result(data)
                except Exception as e:
                    print(f"Erro ao parsear JSON: {e}")
                    self._future_response.set_exception(e)

    async def close(self):
        """Fecha o browser e encerra o Playwright."""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        print("Browser e Playwright finalizados.")
