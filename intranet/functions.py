from django.http import JsonResponse, HttpResponse
import simplejson as json
from intranet.models import Comment, Post
from django.views.decorators.csrf import csrf_exempt
from django.template.context_processors import csrf
from django.core import serializers
from django.contrib.auth.models import User

@csrf_exempt
def post_comment(request):
	
	if request.method == 'POST' and request.is_ajax():
		comment = request.POST['comment'].encode('utf-8')
		parent_post = int(str(request.POST['parent_post_id']))
		parent_post = Post.objects.get(id=parent_post)
		
		comment_object = Comment(comment=comment, author=request.user, post = parent_post)
		comment_object.save()
		
		try:
			parent_post.comments.append(comment_object.id)
			parent_post.save()
		except AttributeError:
			parent_post.comments = list()
			parent_post.comments.append(comment_object.id)
			parent_post.save()	
		parent_post.save()
		data = {
			'comment':Comment.objects.filter(id = comment_object.id).values()[0],
			'author':comment_object.author.get_full_name()			
			}
		#data = serializers.serialize("json",Comment.objects.filter(id=comment_object.id))
		return JsonResponse(data)
	return HttpResponse(request.method)
