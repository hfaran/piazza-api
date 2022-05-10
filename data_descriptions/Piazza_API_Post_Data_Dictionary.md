# Piazza-API: Post Query Data Dictionary

When querying a post with Piazza-API, you will receive a nested dictionary object for each post. Each of these post dictionaries has several top-level and nested properties which are enumerated below. The list and their descriptions are not fully complete and is a best efforts compilation of their meaning, values, and structure. 

## Top Level Post Properties

**id** (str): unique id/ hash of the given primary thread ;

**folders** (list of strings): the folder names where the piazza post is stored; If the post is stored in a sub-directory the parent directory path is repeated and included in the listing for that entry;

**nr** (int):unique post id of the parent thread;

**data** (dict): seems to be a deprecated object consistently returns "{'embed_links': []}";

**created** (str):timestamp as string of the date of initial post creation. timestamp format: yyyy-MM-dd'T'HH:mm:ss'Z' (ISO8601 standard);

**bucket_order** (int): Within piazza threads are collapsed into "buckets" by recency with pinned posts always at "bucket == 0" and later posts falling into subsequent buckets. This number represents this posts' given bucket assignment at the time of scraping;

**bucket_name** (str): Name of the bucket where the thread is stored example "Today", "Pinned", "Yesterday"... etc.;

**no_answer_followup** (int): Count of posts marked unresolved within thread. Does not include responded questions/notes only directly unresolved posts;

**change_log** (list of dicts): list of change_dictionary(s) see change_dictionary;

**history_size** (int): length of the history object;

**History** (list of dicts): The history list tracks all of the changes made to the initial primary post in a given thread. each of these changes is stored as a dict of history_changes (including initial post) see history_changes dict for more details;

**type** (str): indicates the type of post the initial primary thread was, one of:
            note: thread where you don't need an answer (won't be marked unresolved or non-responded to)
            question: thread where you need a response (will be marked unresolved if public or non-responded to if private initially)
            poll: in-class poll

**tags** (list of strings): indicates internal piazza post tag designations these include strings representing the folder the post is stored in as well:
                    'unanswered': post is unresolved or non-responded to
                    'instructor-note': if the post was created by an instructor
                    'pin': if the post is a pinned post 
                    'student' if the post is student originated

**config** (dict): details about the user session configuration see post_configuration_dictionary for further details;

**tag_good** (list of dicts): This field represents a list of post endorsement information as a dict see endorsement_dict for further details;

**tag_good_arr** (list of strings): We believe this entry is used to expose the endorser's for a child post to the parent thread. This item only contains endorser ids as a list;

**children** (nested list of dicts): The children property holds all of the primary thread's follow-up and feedback threads. The first level of the list includes all follow-up posts as their own objects
The second level of the nesting represents feedback post objects that correspond to their parent follow-up post object. See followup_children_dict and feedback_children_dict for further details;

**unique_views** (int): number of unique views the thread has had;

**uid** (str): user id hash associated with the post creator not present if it was your post;

**status** (string): 'active' if the post is live 'inactive' if post deleted or removed;

**drafts** (dict): contains draft versions of the post / edits if multiple users or single user has uncommitted changes to the post;

**request_instructor** (int): indicates the number of instructors that have been tagged in an unresolved thread;

**request_instructor_me** (bool): indicates if you are an instructor in the course and you have been tagged by name in an unresolved thread;

**bookmarked** (int): number of students/instructors that have bookmarked/followed the post;

**num_favorites** (int): count of the number of students and instructors that have favorited the thread;

**my_favorite** (bool): indicates if this post is favorited by the user account;

**is_bookmarked** (bool): indicates if this post is bookmarked/followed by the user account;

**is_tag_good** (bool): indicates if the user has personally endorsed this post

**q_edits** (list of dicts): seems deprecated possibly stored edits by admin permissioned users

**i_edits** (list of dicts): seems deprecated possibly stored edits by instructor permissioned users

**s_edits** (list of dicts): seems deprecated possibly stored edits by student permissioned users

**t** (int): unsure looks like an integer representing post id or something similar

**default_anonymity** (bool): indicates if the post is by default set to be anon

**my_post** (bool): indicates if the user is responsible for the post creation

## Inner Level Post Properties

**change_dictionary** (dict): Each change made to the overall thread is logged here as it's own change object dictionary these dicts take the form;
```
        { 'anon' : value indicates if the post was anon if 'no' or if it was an anon post it represents the piazza assigned alias used as a string example "stud" or "calc",
          'uid_a': value is present if user is anon and represents the unique id for the anon user in this thread,
          'uid' : internal piazza user id of the post contributor,
          'data' : only present for initial thread creation change logs is a hash of the posted content,
          'to' : id of the primary post thread which the response was posted to,
          'v': stands for visibility of the post one of:
                all: total post visibility
                private: post is private

          'type': type of edit one of ['create', 'followup', 'feedback','i_answer', 's_answer']
                create: create initial thread
                followup: responses to a thread
                feedback: responses to a follow-up
                i_answer: applied when the change was applied to the collective instructor answer post
                s_answer: applied when the change was applied to the collective student answer post

          'when': ISO8601 timestamp when the change was made,
          'cid': child post unique identifier hash used to link the change logs to the post children object
        }
```

**history_changes** (dict): dict contains the post change history;
```
        { 'anon' : value indicates if the post was anon if 'no' or if it was an anon post it represents the piazza assigned alias used as a string example "stud" or "calc",
          'uid_a': value is present if user is anon and represents the unique id for the anon user in this thread,
          'uid' : internal piazza user id of the post contributor,
          'subject' : the subject line of the message as innerHTML string,
          'created' : ISO8601 timestamp when the change was made
          'content' : content of the post as innerHTML string,
        }
```

**post_configuration_dictionary** (dict): dict for representing the post user's configuration settings;
```
        { 'editor': indicates the type of editor within the piazza post creation which was used one of:
            'rte' : rich text editor
            'plain' : plain text editor
            'me' : markdown editor

          'feed_groups': comma separated hashes of the groups the private post was originally authored to
          'must_read_version': we believe this indicates presence on the reading list if 1 else 0,
          'has_emails_sent': we believe this indicates if at creation the thread bypassed email preferences if so 1 else 0
          'seen': dictionary indicating the counts of students who have and have not seen the post example: {'1014': 0, '338': 1}
            this description in config does not appear to be present in queries originating from an instructor account only student queries show this
        }
```
**endorsement_dict** (dict): dictionary containing the information for post endorsements;
```
        { 'role' : role of the endorser one of 'student' or 'instructor',
          'name' : Piazza public name of endorser as string,
          'endorser': a dictionary containing information about the specific endorser not sure what these hashes mean exactly
          'admin': True/False is the endorser a piazza administrator,
          'photo': photo name of the endorser's piazza profile photo if added,
          'id': endorser user id,
          'photo_url': url for the location of the endorser's student image if added to piazza profile,
          'published': True/False whether the endorser is publicly published on the piazza platform,
          'us': True/False not sure what this value represents,
          'facebook_id': Facebook ID if the endorser has linked Facebook to piazza
        }
```

**followup_children_dict** (dict): dictionary containing the information for follow-up posts;
```
        { 'anon': value indicates if the post was anon if 'no' or if it was an anon post it represents the piazza assigned alias used as a string example "stud" or "calc",
          'folders': seems to be a deprecated object consistently returns "[]" regardless of parent folder,
          'data': seems to be a deprecated object consistently returns "{'embed_links': []}",
          'no_upvotes': integer number of upvotes,
          'subject': post content as string of innerHTML,
          'created': ISO8601 timestamp when the change was made,
          'bucket_order': bucket number for the parent post if the post was unpinned,
          'bucket_name': bucket name for the parent post if the post was unpinned,
          'type': indicates the type of post the initial primary thread was, one of ['note', 'question', 'poll'],
          'tag_good': endorsement dictionaries,
          'tag_good_arr': list of user id's of post endorsers,
          'uid': internal piazza user id of the post contributor,
          'updated': ISO8601 timestamp when changes were last made (if none then original creation timestamp)
          'config': post configuration dictionary
          'children': feedback_children_dict
        }
```

**feedback_children_dict** (dict): dictionary containing the information for feedback posts;
```
        { 'anon': value indicates if the post was anon if 'no' or if it was an anon post it represents the piazza assigned alias used as a string example "stud" or "calc",
              'folders': seems to be a deprecated object consistently returns "[]" regardless of parent folder,
              'data': seems to be a deprecated object consistently returns "{'embed_links': []}",
              'subject': post content as string of innerHTML,
              'created': ISO8601 timestamp when the change was made,
              'bucket_order': bucket number for the parent post if the post was unpinned,
              'bucket_name': bucket name for the parent post if the post was unpinned,
              'type': indicates the type of post the initial primary thread was, one of ['note', 'question', 'poll'],
              'tag_good': endorsement dictionaries,
              'uid': interal piazza user id of the post contributor,
              'children': further nested commentary dictionaries,
              'tag_good_arr': list of user id's of post endorsers,
              'id': post identification id,
              'updated': ISO8601 timestamp when changes were last made (if none then original creation timestamp),
              'config': post configuration dictionary
        }
```

