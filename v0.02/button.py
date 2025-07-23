import pygame


# button class
class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action


query = (
            "SELECT u.username, m.content, m.sent_at FROM messages m  JOIN users u on m.userID =u.userID WHERE m.chatroomID" +
            " IN (SELECT chatroomID FROM chatrom_members WHERE userID = 1 ) ORDER BY m.sent_at ASC")

# def handle_post():
#     global outp, post_input  # post_input is bound to parsed input from the application
#     hasCondition = False
#     outp = ""

#     outp += str(post_input)
#     title = post_input.get('Title', [''])[0]
#     author = post_input.get('Author', [''])[0]
#     isbn = post_input.get('ISBN', [''])[0]
#     publisher = post_input.get('Publisher', [''])[0]
#     year = post_input.get('Year', [''])[0]

#     DBtable = "Books"
#     db = DatabaseConnection()
#     outp += "<p>DB Connected...<br>"

#     query = "SELECT * FROM " + DBtable

#     if title:
#         query += " WHERE Title LIKE '" + title + "'"
#         hasCondition = True
#     if author:
#         if hasCondition:
#             query += " AND Author LIKE '" + author + "'"
#         else:
#             query += " WHERE Author LIKE '" + author + "'"
#             hasCondition = True
#     if isbn:
#         if hasCondition:
#             query += " AND ISBN = " + isbn
#         else:
#             query += " WHERE ISBN = " + isbn
#             hasCondition = True
#     if publisher:
#         if hasCondition:
#             query += " AND Publisher LIKE '" + publisher + "'"
#         else:
#             query += " WHERE Publisher LIKE '" + publisher + "'"
#             hasCondition = True
#     if year:
#         if hasCondition:
#             query += " AND Year = " + year
#         else:
#             query += " WHERE Year = " + year
#             hasCondition = True

#     print(query)
#     outp += "<p>Query is " + query + "<p>\n"
#     results = db.execute_query(query)

#     if results:
#         outp += "Found:<br>\n"
#         for row in results:
#             outp += ', '.join(map(str, row)) + "<br>\n"
#     else:
#         outp += "No results found.<br>\n"
