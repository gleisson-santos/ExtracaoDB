from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime, timedelta

def esperar_sumir(driver):
    """Aguarda elemento desaparecer"""
    wait = WebDriverWait(driver, 30)
    element = wait.until(
        EC.invisibility_of_element_located((By.ID, "j_idt24_modal")))

def esperar_clicavel(variavel, driver):
    """Aguarda elemento ficar clicável"""
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.ID, variavel)))

def abrir_filtro(filtro, driver):
    """Abre e seleciona o filtro"""
    esperar_clicavel("form-filtroAcss-toolbox-btn-search", driver)
    driver.find_element(by=By.ID, value="form-filtroAcss-btnOpenDlgPrefs").click()
    esperar_clicavel(filtro, driver)
    driver.find_element(by=By.ID, value=filtro).click()

def filtro_data(data1, data2, driver):
    """Define o filtro de datas"""
    time.sleep(1)
    driver.find_element(
        by=By.ID, value="form-filtroAcss-dataId-dataTipo-beginDate").clear()
    time.sleep(1)
    driver.find_element(
        by=By.ID, value="form-filtroAcss-dataId-dataTipo-beginDate").click()
    time.sleep(1)
    driver.find_element(
        by=By.ID, value="form-filtroAcss-dataId-dataTipo-beginDate").send_keys(data1)
    time.sleep(1)
    driver.find_element(
        by=By.ID, value="form-filtroAcss-dataId-dataTipo-endDate").clear()
    time.sleep(1)
    driver.find_element(
        by=By.ID, value="form-filtroAcss-dataId-dataTipo-endDate").click()
    time.sleep(1)
    driver.find_element(
        by=By.ID, value="form-filtroAcss-dataId-dataTipo-endDate").send_keys(data2)
    time.sleep(1)

def trocar_localidade(localidade, bairro, driver):
    """Troca localidade e bairro"""
    time.sleep(1)
    esperar_sumir(driver)
    driver.find_element(
        by=By.ID, value="form-filtroAcss-solicitacaoLocalidadeId-j_idt198-cb-input").clear()
    time.sleep(1)
    esperar_sumir(driver)
    driver.find_element(
        by=By.ID, value="form-filtroAcss-solicitacaoLocalidadeId-j_idt198-cb-input").click()
    time.sleep(1)
    esperar_sumir(driver)
    driver.find_element(
        by=By.ID, value="form-filtroAcss-solicitacaoLocalidadeId-j_idt198-cb-input").send_keys(localidade)
    time.sleep(1)
    esperar_sumir(driver)
    driver.find_element(
        by=By.ID, value="form-filtroAcss-solicitacaoBairroId-j_idt205-bairro-input").clear()
    time.sleep(1)
    esperar_sumir(driver)
    driver.find_element(
        by=By.ID, value="form-filtroAcss-solicitacaoBairroId-j_idt205-bairro-input").click()
    time.sleep(1)
    esperar_sumir(driver)
    driver.find_element(
        by=By.ID, value="form-filtroAcss-solicitacaoBairroId-j_idt205-bairro-input").send_keys(bairro)
    esperar_sumir(driver)
    time.sleep(1)

def pesq_exp(driver, callback=None):
    """Pesquisa e exporta dados"""
    esperar_sumir(driver)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.ID, "form-filtroAcss-toolbox-btn-search"))).click()
    time.sleep(2)
    esperar_sumir(driver)
    driver.find_element(
        by=By.ID, value="form-filtroAcss-toolbox-btn-search").click()
    esperar_sumir(driver)
    time.sleep(2)
    try:
        driver.find_element(
            by=By.ID, value="form-grid-grid-exportBtn-exportarxls").click()
        time.sleep(2)
        if callback:
            callback("Planilha exportada com sucesso!")
    except Exception as e:
        if callback:
            callback(f"Erro ao exportar: {str(e)}")

def gerar_datas(data_inicio_str, data_fim_str):
    """Gera lista de datas entre dois períodos"""
    formato_data = '%d/%m/%Y'
    data_inicio = datetime.strptime(data_inicio_str, formato_data)
    data_fim = datetime.strptime(data_fim_str, formato_data)

    datas = []
    delta = timedelta(days=1)

    while data_inicio <= data_fim:
        datas.append(data_inicio)
        data_inicio += delta

    return datas

def definitiva_web(filtro, datas, session_id, callback):
    """
    Função principal de extração adaptada para web
    
    Args:
        filtro: ID do filtro a usar
        datas: Lista de datas para processar
        session_id: ID da sessão para WebSocket
        callback: Função para enviar mensagens de progresso
    """
    # Credenciais (usar variáveis de ambiente em produção)
    user = os.getenv('SCI_USER', 't034183')
    passw = os.getenv('SCI_PASSWORD', 'Caneta2025*')
    url = 'http://sciweb.embasanet.ba.gov.br/sci-web/'

    try:
        # Configurar Chrome
        options = Options()
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_experimental_option("prefs", {
            "download.prompt_for_download": False,
            "download.default_directory": "/tmp"
        })

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        
        callback(f"Iniciando extração com filtro {filtro}")
        driver.get(url)
        time.sleep(1)

        # Login
        callback("Realizando login...")
        randomtag = driver.find_element(
            by=By.ID, value="random-tag").get_attribute('value')
        driver.find_element(
            by=By.ID, value=f"loginForm-usuario-{randomtag}").send_keys(user)
        driver.find_element(
            by=By.ID, value=f"loginForm-senha-{randomtag}").send_keys(passw)
        driver.find_element(by=By.ID, value="loginForm-submit").click()

        # Navegação
        callback("Navegando para consulta geral...")
        esperar_sumir(driver)
        driver.find_element(by=By.ID, value="arvoreSearch").send_keys("gera")
        esperar_sumir(driver)

        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.ID, 'CRSS_anchor')))
        driver.find_element(by=By.ID, value="CRSS_anchor").click()
        driver.switch_to.frame("frame-content")

        callback("Abrindo filtro...")
        abrir_filtro(filtro, driver)
        esperar_sumir(driver)

        # Loop de datas
        for i in range(0, len(datas), 3):
            data_inicio = datas[i].strftime('%d/%m/%Y')
            if i + 2 < len(datas):
                data_fim = datas[i + 2].strftime('%d/%m/%Y')
            else:
                data_fim = datas[-1].strftime('%d/%m/%Y')

            callback(f"Processando datas: {data_inicio} a {data_fim}")
            
            filtro_data(data_inicio, data_fim, driver)
            esperar_sumir(driver)
            
            trocar_localidade("700", "0", driver)
            esperar_sumir(driver)
            pesq_exp(driver, callback)

            esperar_sumir(driver)

            trocar_localidade("900", "0", driver)
            esperar_sumir(driver)
            pesq_exp(driver, callback)
            
            time.sleep(1)

        callback("Extração concluída!")
        driver.quit()

    except Exception as e:
        callback(f"ERRO: {str(e)}")
        try:
            driver.quit()
        except:
            pass
