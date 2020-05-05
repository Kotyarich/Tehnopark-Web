from django.db import migrations

migration = '''
        DROP TRIGGER search_text_update ON questions_question;
        DROP TRIGGER search_title_update ON questions_question;
        
        CREATE FUNCTION questions_trigger() RETURNS trigger AS $$
        begin        
            IF (TG_OP = 'UPDATE') THEN
                UPDATE questions_pgquestionsearch SET search_vector_title=to_tsvector('pg_catalog.english', coalesce(new.title,'')),
                    search_vector_text=to_tsvector('pg_catalog.english', coalesce(new.text,''))
                    WHERE question_id = NEW.id;
                RETURN NEW;
            ELSIF (TG_OP = 'INSERT') THEN
                INSERT INTO questions_pgquestionsearch(question_id, search_vector_title, search_vector_text) 
                    VALUES (new.id, to_tsvector('pg_catalog.english', coalesce(new.title,'')), to_tsvector('pg_catalog.english', coalesce(new.text,'')));
                RETURN NEW;
            END IF;
        end
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE
            ON questions_question FOR EACH ROW EXECUTE PROCEDURE questions_trigger();    
    '''

reverse_migration = '''
        DROP TRIGGER tsvectorupdate ON questions_question;
    '''


def forwards(apps, schema_editor):
    if schema_editor.connection.alias != 'default':
        return
    migrations.RunSQL(migration, reverse_migration)


class Migration(migrations.Migration):
    dependencies = [
        ('questions', '0008_auto_20200505_0332'),
    ]

    operations = [
        migrations.RunPython(forwards),
    ]
