from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blogs.models import Category, Post

class Command(BaseCommand):
    help = "Create editorial categories and ten sample blog posts."
    def handle(self,*args,**options):
        categories = [
            ("Technology","Ideas on software, tools and the digital world."),
            ("Creativity","Making room for better ideas and creative practice."),
            ("Lifestyle","Thoughtful habits for everyday living."),
            ("Learning","Notes on curiosity, growth and lifelong learning."),
            ("Culture","Stories about people, places and perspectives."),
        ]
        catmap = {}
        for name,desc in categories:
            cat, _ = Category.objects.get_or_create(name=name,defaults={"slug":name.lower(),"description":desc})
            catmap[name] = cat
        author, created = User.objects.get_or_create(username="demo_author",defaults={"email":"demo@example.com","first_name":"Alex","last_name":"Morgan"})
        if created: self.stdout.write("Created demo_author (set a password in Django admin before logging in).")
        samples = [
            ("The quiet power of starting small","A practical case for building momentum through tiny, repeatable actions.","Learning"),
            ("Designing a calmer digital workspace","A few intentional choices can make the tools we use feel lighter and more focused.","Technology"),
            ("A field guide to better questions","Curiosity becomes useful when we learn to ask questions that open new doors.","Creativity"),
            ("What a morning walk can teach us","A slower start can create space to notice details that usually pass us by.","Lifestyle"),
            ("The craft of paying attention","Attention is a skill. Like any skill, it grows with patient practice.","Creativity"),
            ("Making technology feel more human","Good digital experiences begin with empathy, clarity and respect for people.","Technology"),
            ("Learning in public, one note at a time","Sharing unfinished thinking can turn private learning into a generous conversation.","Learning"),
            ("The stories hidden in ordinary places","The familiar often becomes interesting when we take the time to look again.","Culture"),
            ("A simple framework for deep work","Protecting a little focused time can change the quality of what we make.","Lifestyle"),
            ("Building a reading habit that lasts","A sustainable reading practice is less about speed and more about returning.","Culture"),
        ]
        for i,(title,excerpt,category) in enumerate(samples):
            Post.objects.get_or_create(title=title,author=author,defaults={
                "content":f"<p>{excerpt}</p><h2>Begin with intention</h2><p>Meaningful progress rarely arrives all at once. It is shaped by small decisions, honest reflection and the willingness to keep learning. Start with one useful step, notice what changes, and build from there.</p><blockquote>Consistency gives good ideas the time they need to grow.</blockquote><p>Try this approach for a week. Keep what works, adjust what does not, and share what you discover with someone else.</p>",
                "excerpt":excerpt,"category":catmap[category],"tags":"ideas, reflection, practice",
                "status":Post.PUBLISHED,"featured":i==0
            })
        self.stdout.write(self.style.SUCCESS("Demo categories and 10 sample posts are ready."))
