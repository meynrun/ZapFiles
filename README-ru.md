![ZapFiles](./assets/ZapFiles-banner.png)

[![Лицензия](https://img.shields.io/github/license/Ileriayo/markdown-badges?style=for-the-badge)](./LICENSE)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)

[![English](https://img.shields.io/badge/English-0078D4?style=for-the-badge&logo=download&logoColor=white)](./README.md)
[![Русский](https://img.shields.io/badge/Русский-D52B1E?style=for-the-badge&logo=download&logoColor=white)](./README-ru.md)

[![Последняя сборка](https://img.shields.io/badge/Скачать%20последнюю%20версию-66CC00?style=for-the-badge&logo=download&logoColor=white)](https://github.com/meynrun/ZapFiles/releases/latest/download/Setup-x64.exe)

### **ZapFiles** - это инструмент для передачи файлов, который обеспечивает конфиденциальность ваших данных благодаря сквозному шифрованию.

# Использование
### Загрузка файла
1. Выберите режим "Скачивание файлов".
2. Введите ключ сервера в поле ввода.
3. Ожидайте, файл будет загружен.

### Отправка фалов
1. Выберите режим "Отправка фалов".
2. Выберите тип IP для передачи файлов:
   - По интернету — для передачи файлов через интернет (требует открытые порты)
   - По локальной сети — для передачи файлов через локальную сеть (например, в одной сети Wi-Fi).
3. Введите имя файла для отправки.
4. Укажите желаемый порт или оставьте его пустым (по умолчанию 8888).
5. Скопируйте ключ сервера и отправьте его получателю для начала передачи.

# Сборка
1. Клонируйте репозиторий: 
```shell
git clone https://github.com/meynrun/ZapFiles.git
```
2. Создайте виртуальное окружение (Linux):
```shell
python3 -m venv .venv
source .venv/Scripts/activate
```
или (Windows)
```shell
python -m venv .venv
.venv\Scripts\activate
```
3. Установите зависимости: 
```shell
pip3 install -r requirements.txt
```
4. Установите [Inno Setup](https://jrsoftware.org/download.php/is.exe)
5. Запустите build.bat

# ToDo
- [x] Выбор порта
- [x] Прогресс бар
- [x] Конфигурационный файл
- [x] Конфигурационный файл для экспериментов
- [x] Раздача файла нескольким клиентам одновременно

# Эксперименты
- [x] Классификация файлов по типу (например, документы, презентации или видео)
- [ ] Пароль для доступа к файлу на сервере

# Возможно в будущем
- [ ] Встроенный проброс портов
- [ ] Промежуточные сервера
- [ ] Система плагинов

# Конфигурация
- **check_for_updates** (bool): переключает проверку обновлений _(по умолчанию: **true**)_
- **language** (str): устанавливает язык, например, **"auto", "en", "ru"** _(по умолчанию: **"auto"**)_
- **enable_emojis** (bool): переключает (почти) все эмодзи _(по умолчанию: **true**)_
- **clear_mode** (str): режим очистки экрана, например, **"ASCII", "ASCII2", "command"** _(по умолчанию: **"ASCII"**)_
- **downloads_path** (str): путь к папке загрузок, например, **"C:/Users/USER/Downloads/ZapFiles Downloads/"**

## Credits
В логотипе приложения используются значки эмодзи из Windows 11, которые являются собственностью Microsoft.
## Disclaimer
Использование значков emoji из Windows 11 регулируется условиями использования Microsoft. Лицензия MIT распространяется на исходный код приложения, но не предоставляет прав на использование интеллектуальной собственности Microsoft за пределами данного приложения.
