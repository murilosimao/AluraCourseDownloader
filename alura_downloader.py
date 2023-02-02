import importlib
import os


def configure():
    imports = ['selenium', 'webdriver-manager', 'tqdm']
    for imp in imports:
        spam_loader = importlib.find_loader(imp)
        found = spam_loader is not None
        if not found:
            print(f'Instalando modulo: {imp}')
            os.system(f'pip install {imp}') 
        
        else:
            print(f'Checando modulo: {imp}')


def main():
    from webdriver_manager.firefox import GeckoDriverManager
    # from webdriver_manager.chrome import ChromeDriverManager
    from selenium import webdriver
    from selenium.webdriver.support.ui import Select
    from selenium.webdriver.common.by import By
    from selenium.webdriver.firefox.service import Service
    import time
    import urllib.request
    from tqdm import tqdm
    import os
    from getpass import getpass
    import base64

    def login_encrypt():
        try:
            with open('.upw') as f:
                result = f.readlines()[0]
                user, password = result.split(' ')

                user = base64.b64decode(user).decode('ascii')
                password = base64.b64decode(password).decode('ascii')

                print(f'Usuário: {user} Autenticado!')
                return user, password


        except IOError:
            user = input('Usuario: ')
            password = getpass('Senha: ')

            user = user.encode('ascii')
            password = password.encode('ascii')

            user = base64.b64encode(user)
            password = base64.b64encode(password)

            with open('.upw', 'w') as f:
                user = str(user).split("'")[1]
                password = str(password).split("'")[1]
                f.write(f'{user} {password}')
                f.close()

            user = base64.b64decode(user).decode('ascii')
            password = base64.b64decode(password).decode('ascii')

            print(f'Usuário: {user} Autenticado!')
            return user, password

    def fazer_login():
        user, password = login_encrypt()
        driver.get('https://cursos.alura.com.br/loginForm?logout')
        email = driver.find_element(By.ID, 'login-email').send_keys(user)
        password = driver.find_element(By.ID, 'password').send_keys(password)
        botao_entrar = driver.find_element(By.XPATH, '//*[@id="form-default"]/button').click()

    def entrar_curso(link):
        driver.get(link)
        nome_curso = link.split('/')[4]
        driver.find_element(By.XPATH, '/html/body/section[2]/section/div[2]/div/div/div/a').click()
        return nome_curso

    def baixar_video(ids, nomes, nome_curso):
        path =  os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop', nome_curso)
        if not os.path.exists(path):
            os.makedirs(path)

        for id,nome in tqdm(zip(ids, nomes)):
            time.sleep(1)
            driver.switch_to.new_window('tab')
            time.sleep(1)
            driver.get(f'https://cursos.alura.com.br/video/diagnostic?taskId={id}')
            driver.execute_script("window.scrollBy(0,250)")
            link_down = driver.find_element(By.XPATH, '/html/body/main/div/div[2]/div/div[1]/video-js/video/source').get_attribute('src')
            urllib.request.urlretrieve(link_down, f'{path}/{id}-{nome}.mp4')
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

    def pegar_id_aula():
        options = driver.find_elements(By.XPATH, '/html/body/section/aside/section[3]/select/option')
        options = len(options)
        aulas_id = []
        nomes_video = []
        

        for opt in range(options):
            select = Select(driver.find_element(By.XPATH, "//select[@class='task-menu-sections-select']"))
            select.select_by_index(opt)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            videos = driver.find_elements(By.XPATH, "//a[@class='task-menu-nav-item-link task-menu-nav-item-link-VIDEO']")
            ids = [video.get_attribute('href').split('/')[-1] for video in videos]
            nomes = [a.text for a in videos]
            driver.execute_script("window.scrollTo(0, 0)")
            driver.refresh()
            for id in ids:
                aulas_id.append(id)

            for nome in nomes:
                nome = nome.split('\n')[1]
                nome = nome.replace('?', '')
                nomes_video.append(nome)

        
        return aulas_id, nomes_video

    links = [
        # 'https://cursos.alura.com.br/course/docker-swarm-cluster-container',
    ]
    
    

    options = webdriver.FirefoxOptions()
    options.headless = True
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
    os.system('cls')

    print('Fazendo Login.')
    fazer_login()

    print('Entrando no curso.')
    # link = input('Link: ')
    for link in links:
        print(link)
        nome_curso = entrar_curso(link)

        print('Analisando Aulas.')
        ids,nomes = pegar_id_aula()

        print('Baixando Aulas:')
        baixar_video(ids, nomes, nome_curso)

    driver.quit()


# configure()
main()


