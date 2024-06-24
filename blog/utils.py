from faker import Faker
from blog.models import Entry, db

def generate_entries(how_many=10):
    fake = Faker()

    for _ in range(how_many):
        post = Entry(
            title=fake.sentence(),
            body='\n\n'.join(fake.paragraphs(15)),  # 15 akapitów w treści
            is_published=True
        )
        db.session.add(post)

    db.session.commit()