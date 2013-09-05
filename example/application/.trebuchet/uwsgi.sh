{% extends base_template %}

{% block command_body %}

export LOG="${LOG_FOLDER}/{{ name }}.log"

# clean-up cache
find {{ app_code }} -name "*.pyc" -delete

# uWSGI script itself.
exec {{ app_env }}/bin/uwsgi --master --die-on-term --show-config  --virtualenv {{ app_env }} --pythonpath {{ app_code }} --module main --callable app --uid hero --gid hero --socket 0.0.0.0:${SECRET_SAUCE_WEB_UWSGI_PORT} --processes 2 --logto $LOG $SERVICE_COMMAND_OPTIONS

{% endblock %}