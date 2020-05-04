from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('questions', '0006_auto_20200504_0347'),
    ]

    migration = '''
        CREATE TRIGGER search_title_update BEFORE INSERT OR UPDATE
        ON questions_question FOR EACH ROW EXECUTE FUNCTION
        tsvector_update_trigger(search_vector_text, 'pg_catalog.english', text);

        CREATE TRIGGER search_text_update BEFORE INSERT OR UPDATE
        ON questions_question FOR EACH ROW EXECUTE FUNCTION
        tsvector_update_trigger(search_vector_title, 'pg_catalog.english', title);
        -- Force triggers to run and populate the text_search column.
        UPDATE questions_question set ID = ID;
    '''

    reverse_migration = '''
        DROP TRIGGER search_text_update ON questions_question;
        DROP TRIGGER search_title_update ON questions_question;
    '''

    operations = [
        migrations.RunSQL(migration, reverse_migration)
    ]
