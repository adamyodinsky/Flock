# TITLE

## Example of how gpt-4 can understand a Trello webhook response payload

```markdown
This is the "action" part of a Trello webhook payload:

  
  {'id': '647710503edc1368012b3498', 'idMemberCreator': '5e241afac0016644f468c6c5', 'data': {'card': {'idList': '64770f7c45d4ab01fff6884d', 'id': '64765103e674abbe18fb9e8c', 'name': 'helo', 'idShort': 4, 'shortLink': 'IcStvitd'}, 'old': {'idList': '647367960a35139ab08f73e3'}, 'board': {'id': '64732651e20f27dc08e2d1cd', 'name': 'api-test', 'shortLink': 'GAg5PkE2'}, 'listBefore': {'id': '647367960a35139ab08f73e3', 'name': 'TODO'}, 'listAfter': {'id': '64770f7c45d4ab01fff6884d', 'name': 'In Progress'}}, 'appCreator': None, 'type': 'updateCard', 'date': '2023-05-31T09:16:00.179Z', 'limits': None, 'display': {'translationKey': 'action_move_card_from_list_to_list', 'entities': {'card': {'type': 'card', 'idList': '64770f7c45d4ab01fff6884d', 'id': '64765103e674abbe18fb9e8c', 'shortLink': 'IcStvitd', 'text': 'helo'}, 'listBefore': {'type': 'list', 'id': '647367960a35139ab08f73e3', 'text': 'TODO'}, 'listAfter': {'type': 'list', 'id': '64770f7c45d4ab01fff6884d', 'text': 'In Progress'}, 'memberCreator': {'type': 'member', 'id': '5e241afac0016644f468c6c5', 'username': 'adamyodinsky1', 'text': 'Adam Yodinsky'}}}, 'memberCreator': {'id': '5e241afac0016644f468c6c5', 'activityBlocked': False, 'avatarHash': '116c9c98d02a03106aebfee595a70d6c', 'avatarUrl': 'https://trello-members.s3.amazonaws.com/5e241afac0016644f468c6c5/116c9c98d02a03106aebfee595a70d6c', 'fullName': 'Adam Yodinsky', 'idMemberReferrer': None, 'initials': 'AY', 'nonPublic': {}, 'nonPublicAvailable': True, 'username': 'adamyodinsky1'}}
  

You are a Trello API expert 

What can you tell me about what happened on the Trello board?
Please break it down step by step to make sure you have the right answer.

```


```markdown
Certainly, let's break down the Trello webhook payload.

1. **Identifying the Action**: The `'type'` field in the payload is `'updateCard'`, which tells us that a card was updated on the Trello board.

2. **Identifying the User**: The `idMemberCreator` field indicates the user who performed the action. According to the `'memberCreator'` dictionary, the member who made this action is `Adam Yodinsky` with the username `adamyodinsky1`.

3. **Identifying the Board**: The `'board'` field in the `'data'` dictionary shows us that the board where the action took place is named `'api-test'`.

4. **Identifying the Card**: In the `'data'` dictionary, the `'card'` field shows that a card named `'helo'` with id `64765103e674abbe18fb9e8c` was updated.

5. **Identifying the Changes**: The `'old'` field in the `'data'` dictionary indicates that the card was originally in a list with the id `647367960a35139ab08f73e3`. In the `'listAfter'` field, we see that the card was moved to a list with the id `64770f7c45d4ab01fff6884d`.

6. **Identifying the Lists**: The `'listBefore'` and `'listAfter'` fields show us the names of the lists where the card was before and after the action. The card was moved from a list named `'TODO'` to a list named `'In Progress'`.

So, to summarize, user Adam Yodinsky updated a card named 'helo' on the 'api-test' board. Specifically, he moved the card from the 'TODO' list to the 'In Progress' list.
```

## Trello webhooks

<https://developer.atlassian.com/cloud/trello/guides/rest-api/webhooks/>

move to "todo queue" list
  label "ai_enabled" exists
  not closed
  list_id == the todo list id


### install ngrok

```sh
brew install ngrok/ngrok/ngrok
```
