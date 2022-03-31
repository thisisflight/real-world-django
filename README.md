Сервис записи на события

Реализовано при помощи фреймворка Django с подключением дополнительных библиотек,<br>
таких как django-cleanup, gunicorn, psycopg2, sentry и других<br>
(полный список в [файле requirements](https://github.com/thisisflight/real-world-django/blob/main/requirements.txt))

Реализованы смена и сброс пароля для пользователя, [код представления](https://github.com/thisisflight/real-world-django/blob/main/accounts/views.py#L78)<br>
Реализованы фикстуры для заполнения базы данных категориями, событиями, пользователями, записями на события.<br>
Реализован простой сервис отправки уведомлений пользователям по e-mail посредством модуля threading и подключением SMTP-клиента Яндекса, [код представления](https://github.com/thisisflight/real-world-django/blob/cf41fdd93395f879b694f40d117dd276a7eca3b8/mail/api.py)<br>

Настройки проекта разделены на:<br>
dev-версию c легковесной базой данных SQLite3 и отладочной библиотекой django-debug-toolbar для контроля запросов в ORM;<br>
preprod-версию с подключением sentry;<br>
prod-версию с sentry и PostgreSQL<br>

Верстка на Bootstrap, интегрирована и расширена при помощи шаблонов Django, реализованы многие built-in фильтры, а также применены custom фильтры и теги.<br>
Применены django messages для вывода информации пользователю о записи на событие (или о том, что пользователь уже подписан), о добавление события в избранное (либо уведомление, что событие уже в избранном)<br>

[Стартовая страница](http://34.88.143.158/) - простой вывод событий и отзывов, [код представления](https://github.com/thisisflight/real-world-django/blob/main/main/views.py)<br>
[Cтраница списка событий](http://34.88.143.158/events/list/) - реализация вывода списка с пагинацией и фильтрацией GET-запросом, [код представления](https://github.com/thisisflight/real-world-django/blob/main/events/views.py#L24)<br>
[Детальная страница события](http://34.88.143.158/events/detail/32/) - вывод отдельного события и отзывов на него от посетителей, возможность записаться на событие или добавить его в избранное (для зарегистрированных пользователей), [код представления](https://github.com/thisisflight/real-world-django/blob/main/events/views.py#L67)<br>
![detailview](https://user-images.githubusercontent.com/86616350/161053878-b71f0a40-e0ac-4c98-b57c-95ffd2695913.gif)
<br>
Функционал для зарегистрированных пользователей:<br>
Cоздание события
<br>[код представления](https://github.com/thisisflight/real-world-django/blob/main/events/views.py#L67)
![createview](https://user-images.githubusercontent.com/86616350/161050581-f103ce1e-738c-4cce-a17d-fe2a8b173b60.gif)
<br>
Редактирование события
<br>[код представления](https://github.com/thisisflight/real-world-django/blob/main/events/views.py#L95)<br>
На странице редактируемого события можно просмотреть информацию о подписчиках, отзывах, а также удалить событие
![updateview](https://user-images.githubusercontent.com/86616350/161052434-d73b60d3-632a-41aa-b325-fb9703d19b20.gif)
Личный кабинет<br>
Реализована возможность смены изображения профиля, выведены все события, на которые подписан пользователь, оценка события (если есть) и отзыв на событие, если оставлен,
[код представления](https://github.com/thisisflight/real-world-django/blob/main/accounts/views.py#L57)
![profile](https://user-images.githubusercontent.com/86616350/161055294-8881999e-7b8a-4f36-a3e4-bba9465ac5e6.gif)
<br>
