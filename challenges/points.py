# from firebase_admin import firestore
# from media.cert import firebase_initialization

# from posts.serializers import PostSerializer


# def updatePoints(challenge, post, points: int):
#     firebase_initialization()
#     db = firestore.client()
#     post_data = PostSerializer(instance = post).data
#     db.collection("challenges").document(challenge).collection("posts").document(
#         user
#     ).update({"points": firestore.Increment(points)})
