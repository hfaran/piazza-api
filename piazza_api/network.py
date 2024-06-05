from collections import namedtuple
import time
from .rpc import PiazzaRPC


################
# Feed Filters #
################

class FeedFilter(object):
    pass

class UnreadFilter(FeedFilter):
    """Filter through only posts with unread content in feed"""
    def __init__(self):
        pass

    def to_kwargs(self):
        return dict(updated=True)

class FollowingFilter(FeedFilter):
    """Filter through only posts that you are following in feed"""
    def __init__(self):
        pass

    def to_kwargs(self):
        return dict(following=True)

class FolderFilter(FeedFilter):
    """Filter only posts in ``folder_name`` in your feed

    :type folder_name: str
    :param folder_name: Name of folder to show posts from in feed
    """
    def __init__(self, folder_name):
        self.folder_name = folder_name

    def to_kwargs(self):
        return dict(folder=True, filter_folder=self.folder_name)


###########
# Network #
###########

class Network(object):
    """Abstraction for a Piazza "Network" (or class)

    :param network_id: ID of the network
    :param session: requests.Session object containing cookies used for
        authentication
    """
    def __init__(self, network_id, session):
        self._nid = network_id
        self._rpc = PiazzaRPC(network_id=self._nid)
        self._rpc.session = session

        ff = namedtuple('FeedFilters', ['unread', 'following', 'folder'])
        self._feed_filters = ff(UnreadFilter, FollowingFilter, FolderFilter)

    @property
    def feed_filters(self):
        """namedtuple instance containing FeedFilter classes for easy access

        :rtype: namedtuple
        :returns: namedtuple with unread, following, and folder attributes
            mapping to filters
        """
        return self._feed_filters

    #########
    # Posts #
    #########

    def get_post(self, cid):
        """Get data from post `cid`

        :type  cid: str|int
        :param cid: This is the post ID to get
        :rtype: dict
        :returns: Dictionary with all data on the post
        """
        return self._rpc.content_get(cid=cid)

    def iter_all_posts(self, limit=None, sleep=0):
        """Get all posts visible to the current user

        This grabs you current feed and ids of all posts from it; each post
        is then individually fetched. This method does not go against
        a bulk endpoint; it retrieves each post individually, so a
        caution to the user when using this.

        :type limit: int|None
        sleep:int -- If given, will allow to actually iterate through all of 
            Piazza channel's posts without getting kicked or banned by Piazza.
            Around 1 second works in practice if you're iterating through
            a lot of posts.
        :param limit: If given, will limit the number of posts to fetch
            before the generator is exhausted and raises StopIteration.
            No special consideration is given to `0`; provide `None` to
            retrieve all posts.
        :returns: An iterator which yields all posts which the current user
            can view
        :rtype: generator
        """
        feed = self.get_feed(limit=999999, offset=0)
        cids = [post['id'] for post in feed["feed"]]
        if limit is not None:
            cids = cids[:limit]
        for cid in cids:
            time.sleep(sleep)
            yield self.get_post(cid)

    def create_post(self, post_type, post_folders, post_subject, post_content, is_announcement=0, bypass_email=0, anonymous=False):
        """Create a post

        It seems like if the post has `<p>` tags, then it's treated as HTML,
        but is treated as text otherwise. You'll want to provide `content`
        accordingly.

        :type post_type: str
        :param post_type: 'note', 'question'
        :type post_folders: str
        :param post_folders: Folder to put post into
        :type post_subject: str
        :param post_subject: Subject string
        :type post_content: str
        :param post_content: Content string
        :type is_announcement: bool
        :param is_announcement:
        :type bypass_email: bool
        :param bypass_email:
        :type anonymous: bool
        :param anonymous:
        :rtype: dict
        :returns: Dictionary with information about the created post.
        """
        params = {
            "anonymous": "yes" if anonymous else "no",
            "subject": post_subject,
            "content": post_content,
            "folders": post_folders,
            "type": post_type,
            "config": {
                "bypass_email": bypass_email,
                "is_announcement": is_announcement
            }
        }

        if bypass_email:
            params["prof_override"] = True

        return self._rpc.content_create(params)

    def create_followup(self, post, content, anonymous=False, instructor=False):
        """Create a follow-up on a post `post`.

        It seems like if the post has `<p>` tags, then it's treated as HTML,
        but is treated as text otherwise. You'll want to provide `content`
        accordingly.

        :type  post: dict|str|int
        :param post: Either the post dict returned by another API method, or
            the `cid` field of that post.
        :type  content: str
        :param content: The content of the followup.
        :type  anonymous: bool
        :param anonymous: Whether or not to post anonymously.
        :rtype: dict
        :returns: Dictionary with information about the created follow-up.
        """
        try:
            cid = post["id"]
        except KeyError:
            cid = post

        params = {
            "cid": cid,
            "type": "followup",
            
            # For followups, the content is actually put into the subject.
            "subject": content,
            "content": "",
            "config": {
                "editor": "rte",
                "ionly": True if instructor else False,
            },
            "anonymous": "yes" if anonymous else "no",
        }
        return self._rpc.content_create(params)

    def create_instructor_answer(self, post, content, revision, anonymous=False):
        """Create an instructor's answer to a post `post`.

        It seems like if the post has `<p>` tags, then it's treated as HTML,
        but is treated as text otherwise. You'll want to provide `content`
        accordingly.

        :type  post: dict|str|int
        :param post: Either the post dict returned by another API method, or
            the `cid` field of that post.
        :type  content: str
        :param content: The content of the answer.
        :type  revision: int
        :param revision: The number of revisions the answer has gone through.
            The first responder should out 0, the first editor 1, etc.
        :type  anonymous: bool
        :param anonymous: Whether or not to post anonymously.
        :rtype: dict
        :returns: Dictionary with information about the created answer.
        """
        try:
            cid = post["id"]
        except KeyError:
            cid = post

        params = {
            "cid": cid,
            "type": "i_answer",
            "content": content,
            "revision": revision,
            "anonymous": "yes" if anonymous else "no",
        }
        return self._rpc.content_instructor_answer(params)

    def create_reply(self, post, content, anonymous=False):
        """Create a reply to a followup

        It seems like if the post has `<p>` tags, then it's treated as HTML,
        but is treated as text otherwise. You'll want to provide `content`
        accordingly.
        :type  post: dict|str|int
        :param post: Either the post dict returned by another API method, or
            the `cid` field of that post.
        :type  subject: str
        :param content: The content of the followup.
        :type  anonymous: bool
        :param anonymous: Whether or not to post anonymously.
        :rtype: dict
        :returns: Dictionary with information about the created follow-up.
        """
        try:
            cid = post["id"]
        except KeyError:
            cid = post

        params = {
            "cid": cid,
            "type": "feedback",

            # For replies, the content is actually put into the subject.
            "subject": content,
            "content": "",

            "anonymous": "yes" if anonymous else "no",
        }
        return self._rpc.content_create(params)

    def update_post(self, post, content):
        """Update post content by cid

        :type  post: dict|str|int
        :param post: Either the post dict returned by another API method, or
            the `cid` field of that post.
        :type  subject: str
        :param content: The content of the followup.
        :rtype: dict
        :returns: Dictionary with information about the updated post.
        """
        try:
            cid = post["id"]
        except KeyError:
            cid = post
        except TypeError:
            cid = post

        params = {
            "cid": cid,
            # For updates, the content is put into the subject.
            "subject": content,
        }
        return self._rpc.content_update(params)

    def mark_as_duplicate(self, duplicated_cid, master_cid, msg=''):
        """Mark the post at ``duplicated_cid`` as a duplicate of ``master_cid``

        :type  duplicated_cid: int
        :param duplicated_cid: The numeric id of the duplicated post
        :type  master_cid: int
        :param master_cid: The numeric id of an older post. This will be the
            post that gets kept and ``duplicated_cid`` post will be concatinated
            as a follow up to ``master_cid`` post.
        :type msg: string
        :param msg: the optional message (or reason for marking as duplicate)
        :returns: True if it is successful. False otherwise
        """
        content_id_from = self.get_post(duplicated_cid)["id"]
        content_id_to = self.get_post(master_cid)["id"]
        params = {
            "cid_dupe": content_id_from,
            "cid_to": content_id_to,
            "msg": msg
        }
        return self._rpc.content_mark_duplicate(params)

    def resolve_post(self, post):
        """Mark post as resolved

        :type  post: dict|str|int
        :param post: Either the post dict returned by another API method, or
            the `cid` field of that post.
        :returns: True if it is successful. False otherwise
        """
        try:
            cid = post["id"]
        except KeyError:
            cid = post

        params = {
            "cid": cid,
            "resolved": "true"
        }

        return self._rpc.content_mark_resolved(params)

    def pin_post(self, post, unpin=False):
        """Pin/Unpin post

        :type  post: dict|str|int
        :param post: Either the post dict returned by another API method, or
            the `cid` field of that post.
        :param unpin: Whether the post should be unpinned.
        :returns: True if it is successful. False otherwise
        """
        try:
            cid = post['id']
        except KeyError:
            cid = post

        params = {
            "cid": cid,
        }

        return self._rpc.content_pin(params, unpin=unpin)

    def delete_post(self, post):
        """ Deletes post by cid

        :type  post: dict|str|int
        :param post: Either the post dict returned by another API method, the post ID, or
            the `cid` field of that post.
        :rtype: dict
        :returns: Dictionary with information about the post cid.
        """

        try:
            cid = post['id']
        except KeyError:
            cid = post
        except TypeError:
            post = self.get_post(post)
            cid = post['id']

        params = {
            "cid": cid,
        }

        return self._rpc.content_delete(params)

    def add_feedback(self, post):
        """Marks a post as a good note
        :type post: dict|str|int
        :param post: Either the post dict returned by another API method, the post ID, or
            the `cid` field of that post.
        :rtype: dict
        :returns: Status `'OK'` if adding feedback was successful.
         """

        try:
         cid = post['id']
        except KeyError:
         cid = post
        except TypeError:
            post = self.get_post(post)
            cid = post['id']

        params = {
            "cid": cid,
            "type": "tag_good"
        }

        return self._rpc.content_add_feedback(params)

    def remove_feedback(self, post):
        """Unmarks a post as a good note
        :type post: dict|str|int
        :param post: Either the post dict returned by another API method, the post ID, or
            the `cid` field of that post.
        :rtype: dict
        :returns: Status `'OK'` if removing feedback was successful.
         """

        try:
         cid = post['id']
        except KeyError:
         cid = post
        except TypeError:
            post = self.get_post(post)
            cid = post['id']

        params = {
            "cid": cid,
            "type": "tag_good"
        }

        return self._rpc.content_remove_feedback(params)

    #########
    # Users #
    #########

    def get_users(self, user_ids):
        """Get a listing of data for specific users ``user_ids`` in
        this network

        :type  user_ids: list
        :param user_ids: A list of user ids (strings). These are the same
            ids that are returned by get_all_users.
        :returns: Python object containing returned data, a list
            of dicts containing user data.
        :rtype: list
        """
        return self._rpc.get_users(user_ids=user_ids)

    def iter_users(self, user_ids):
        """Same as ``Network.get_users``, but returns an iterable instead

        :rtype: listiterator
        """
        return iter(self.get_users(user_ids=user_ids))

    def get_all_users(self):
        """Get a listing of data for all users in this network

        :rtype: list
        :returns: Python object containing returned data, a list
            of dicts containing user data.
        """
        return self._rpc.get_all_users()

    def iter_all_users(self):
        """Same as ``Network.get_all_users``, but returns an iterable instead

        :rtype: listiterator
        """
        return iter(self.get_all_users())

    def add_students(self, student_emails):
        """Add students with ``student_emails`` to the network

        Piazza will email these students with instructions to
        activate their account.

        :type  student_emails: list of str
        :param student_emails: A listing of email addresses to enroll
            in the network (or class). This can be a list of length one.
        :rtype: list
        :returns: Python object containing returned data, a list
            of dicts of user data of all of the users in the network
            including the ones that were just added.
        """
        return self._rpc.add_students(student_emails=student_emails)

    def remove_users(self, user_ids):
        """Remove users with ``user_ids`` from this network

        :type  user_ids: list of str
        :param user_ids: a list of user ids. These are the same
            ids that are returned by get_all_users.
        :rtype: list
        :returns: Python object containing returned data, a list
            of dicts of user data of all of the users remaining in
            the network after users are removed.
        """
        return self._rpc.remove_users(user_ids=user_ids)

    ########
    # Feed #
    ########

    def get_feed(self, limit=100, offset=0):
        """Get your feed for this network

        Pagination for this can be achieved by using the ``limit`` and
        ``offset`` params

        :type limit: int
        :param limit: Number of posts from feed to get, starting from ``offset``
        :type offset: int
        :param offset: Offset starting from bottom of feed
        :rtype: dict
        :returns: Feed metadata, including list of posts in feed format; this
            means they are not the full posts but only in partial form as
            necessary to display them on the Piazza feed. For example, the
            returned dicts only have content snippets of posts rather
            than the full text.
        """
        return self._rpc.get_my_feed(limit=limit, offset=offset)

    def get_filtered_feed(self, feed_filter):
        """Get your feed containing only posts filtered by ``feed_filter``

        :type feed_filter: FeedFilter
        :param feed_filter: Must be an instance of either: UnreadFilter,
            FollowingFilter, or FolderFilter
        :rtype: dict
        """
        assert isinstance(feed_filter, (UnreadFilter, FollowingFilter,
                                        FolderFilter))
        return self._rpc.filter_feed(**feed_filter.to_kwargs())

    def search_feed(self, query):
        """Search for posts with ``query``, returned in feed format

        :type query: str
        :param query: The search query; should just be keywords for posts
            that you are looking for
        :rtype: dict
        """
        return self._rpc.search(query=query)

    ##############
    # Statistics #
    ##############

    def get_statistics(self):
        """Get statistics for class

        :rtype: dict
        :returns: Statistics for class that are viewable on the Statistics
            page on the Piazza web UI
        """
        return self._rpc.get_stats()
