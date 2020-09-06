# Google-translator-GUI
## Python & GTK 3
Автоматический переводчик без использования Google.API

Переводит со всех доступных в Google языков на русский. С русского только на английский.

![screenshot](https://github.com/delvin-fil/Google-translator-GUI/blob/master/screenshot.png)

### Оглавление:
* [Зависимости](https://github.com/delvin-fil/Google-translator-GUI#%D0%B7%D0%B0%D0%B2%D0%B8%D1%81%D0%B8%D0%BC%D0%BE%D1%81%D1%82%D0%B8)
* [Установка зависимостей](https://github.com/delvin-fil/Google-translator-GUI#%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0-%D0%B7%D0%B0%D0%B2%D0%B8%D1%81%D0%B8%D0%BC%D0%BE%D1%81%D1%82%D0%B5%D0%B9)
* [Установка](https://github.com/delvin-fil/Google-translator-GUI#%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0)
* [Привязка переводчика к горячей клавише](https://github.com/delvin-fil/Google-translator-GUI#%D0%BF%D1%80%D0%B8%D0%B2%D1%8F%D0%B7%D0%BA%D0%B0-%D0%BF%D0%B5%D1%80%D0%B5%D0%B2%D0%BE%D0%B4%D1%87%D0%B8%D0%BA%D0%B0-%D0%BA-%D0%B3%D0%BE%D1%80%D1%8F%D1%87%D0%B5%D0%B9-%D0%BA%D0%BB%D0%B0%D0%B2%D0%B8%D1%88%D0%B5)

---
### Зависимости
1. **Python 3.6+**
2. Библиотека **pygobject**
3. Библиотека **requests**
4. Библиотека **langdetect**
5. Библиотека **translators**

---
### Установка зависимостей
#### Ubuntu/Mint/Debian:
```shell
sudo apt-get install python3.6 python3-pip python3-gi python3-gi-cairo gir1.2-gtk-3.0
pip3.6 install --user requests langdetect translators 
```
#### CentOS:
```shell
sudo yum install -y https://centos8.iuscommunity.org/ius-release.rpm
sudo yum update
sudo yum install -y python36u python36u-libs python36u-devel python36u-pip
pip3.6 install --user requests langdetect translators
```
#### RedHat:
```shell
su
yum install gcc openssl-devel bzip2-devel sqlite-devel
cd /usr/src
wget https://www.python.org/ftp/python/3.6.9/Python-3.6.9.tgz
tar xzf Python-3.6.9.tgz
cd Python-3.6.9
./configure --enable-optimizations
make altinstall
pip3.6 install --user requests langdetect translators
```
#### Gentoo:
```shell
sudo USE="cairo" PYTHON_TARGETS="python3_6" emerge dev-python/pygobject -av
sudo emerge dev-python/requests langdetect translators -aqv
pip3.6 install --user requests langdetect translators # для свежей версии модуля
```
#### FreeBSD/DragonFly 
информация от [Tupoll](https://github.com/tupoll)
```shell
pkg install pygobject3-common
pkg install py36-pip
ln -s /usr/local/bin/pip-3.6 /usr/local/bin/pip
pip install --user requests langdetect translators
```

---
## Установка

```
git clone https://github.com/delvin-fil/Google-translator-GUI.git
cd Google-translator-GUI
chmod +x translatorgtk.py
```

---
## Привязка переводчика к горячей клавише

> Так как DE/WM существует довольно много, опишу лишь IceWM, Lumina и Gnome<br>
> добавлено Awesome

### IceWm
- Открыть файл $HOME/.icewm/keys
- Добавить строку<br> 
	```key "Ctrl+1" /path_to/yatrans-gtk.py```
- Перезапусть IceWM<br>
	```Меню >  Выход... > Перезапуск IceWM```

### Lumina
- Меню > Настройки > Настройки рабочего стола > Горячие клавиши > Расширенный редактор
- Добавить строку<br>
	```Control 1 :Exec /path_to/yatrans-gtk.py```

### Gmome 3
- Меню > параметры системы > клавиатура > комбинации клавиш

### Awesome
Спасибо [Tupoll](https://github.com/tupoll) за подсказку<br>
Комбинация клавиш **Alt**+**y** 

- открыть файл $HOME/.config/awesome/rc.lua
- Добавить строку<br>
	```LUA
	-- если следующая строка будет в конце текста, последняя запятая не нужна
	awful.key({ "Mod1", }, "y", function() awful.spawn("sh -c $HOME/path/to/yatrans-gtk.py")end),
	```

Шрифт Menlo Regular указанный в коде присутствует.
```python
 self.textview.modify_font(Pango.FontDescription('Menlo Regular 24'))
 ```