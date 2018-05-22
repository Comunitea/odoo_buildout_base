# Buildout base para proyectos con Odoo y PostgreSQL
Odoo 11.0 en el base, PostgreSQL 10.3 , python3, con supervisor
- Buildout crea cron para iniciar Supervisord después de reiniciar (esto no lo he probado)
- Supervisor ejecuta PostgreSQL, más info http://supervisord.org/
- También ejecuta la instancia de PostgreSQL
- Si existe un archivo dump.sql, el sistema generará la base de datos con ese dump
- Si existe  un archivo frozen.cfg es el que se debeía usar ya que contiene las revisiones aprobadas
- PostgreSQL se compila y corre bajo el usuario user (no es necesario loguearse como root), se habilita al autentificación "trust" para conexiones locales. Más info en more http://www.postgresql.org/docs/9.3/static/auth-methods.html
- Existen plantillas para los archivo de configuración de Postgres que se pueden modificar para cada proyecto.


# Uso (adaptado)
En caso de no haberse hecho antes en la máquina en la que se vaya a realizar, instalar las dependencias que mar Anybox
- Añadir el repo a /etc/apt/sources.list:
```
$ deb http://apt.anybox.fr/openerp common main
```
- Si se quiere añadir la firma. Esta a veces tarda mucho tiempo o incluso da time out. Es opcional meterlo
```
$ sudo apt-key adv --keyserver hkp://subkeys.pgp.net --recv-keys 0xE38CEB07
```
- Instalar dependencias python3
```
$ sudo apt-get install python3-dev
```
- Actualizar e instalar
```
$ sudo apt-get update
$ sudo apt-get install openerp-server-system-build-deps
```
- Para poder compilar e instalar postgres
```
$ sudo apt-get install libreadline-dev
```
- Crear un virtualenv dentro de la carpeta del respositorio. Esto podría ser opcional, obligatorio para desarrollo o servidor de pruebas, tal vez podríamos no hacerlo para un despliegue en producción. Si no está instalado, instalar el paquete de virtualenv. Es necesario tener la versión que se instala con easy_install o con pip, desinstalar el paquete python-virtualenv si fuera necesario e instalarlo con easy_install
```
$ sudo easy_install virtualenv
$ virtualenv -p python3.5 sandbox
```
- Ahora procedemos a ejecutar el buildout en nuestro entorno virtual
```
$ sandbox/bin/python3.5 bootstrap.py -c [archivo_buildout]
```
- Lanzar buildout (el -c [archivo_buildout] se usa cuando no tiene el nombre por defecto buildout.cfg)
```
$ bin/buildout -c [archivo_buildout]
```
- Actualmente supervisor no funciona en python3, por lo que si no se instala manualmente es necesario lanzar postgres y odoo con los comandos
```
$ parts/postgres/bin/postmaster --config-file=etc/postgresql.conf
$ bin/start_odoo
```

- Puede que de error, hay que lanzar el supervisor y volver a hacer bin/buildout:
```
$ bin/supervisord
$ bin/buildout -c [archivo_buildout]
```
- Conectarse al supervisor con localhost:9002
- Si fuera necesario hacer update all, se puede parar desde el supervisor y en la consola hacer:
```
$ cd bin
$ ./upgrade_odoo
```
- odoo se lanza en el puerto 9069 (se pude configurar en otro)

## Securizar el acceso al supervisor
```
$ sudo apt-get install iptables
$ sudo iptables -A INPUT -i lo -p tcp --dport 9002 -j ACCEPT
$ sudo iptables -A INPUT -p tcp --dport 9002 -j DROP
$ sudo apt-get install iptables-persistent (marcamos "yes" en las preguntas que nos hace al instalarse)
```

## Configurar Odoo
Archivo de configuración: etc/odoo.cfg, si sequieren cambiar opciones en  odoo.cfg, no se debe editar el fichero,
si no añadirlas a la sección [odoo] del buildout.cfg
y establecer esas opciones .'add_option' = value, donde 'add_option'  y ejecutar buildout otra vez.

Por ejemplo: cambiar el nivel de logging de odoo
```
'buildout.cfg'
...
[odoo]
options.log_handler = [':ERROR']
...
```

Si se quiere ejecutar más de una instancia de odoo, se deben cambiar los puertos,
please change ports:
```
odoo_xmlrpc_port = 9069  (8069 default odoo)
odoo_xmlrpcs_port = 9071 (8071 default odoo)
supervisor_port = 9002      (9001 default supervisord)
postgres_port = 5434        (5432 default postgres)
```

# Contributors

## Creators

Rastislav Kober, http://www.kybi.sk
