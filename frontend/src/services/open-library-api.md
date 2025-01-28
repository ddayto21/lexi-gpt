## Subject Search

There are multiple ways to search for books by a subject. The primary way is to use the subject: field which will do a fuzzy search for any books with subjects containing your search (e.g. subject:happy would match a subject of "happy feet"). This is also the case for place, time, and person.

An exact subject match can be performed using the subject_key: field. Presently, this value needs to be normalized such that spaces and special characters like / become underscores and the entire term becomes lowercased. For instance (a subject like "Metropolitan Museum of Art (New York, N.Y.)" becomes metropolitan_museum_of_art_(new_york_n.y.)). Here's the code behind the scenes for those who need more details. Note that _key can be added to place, time, and person to achieve the same exact matching capabilities.

    place:rome will find you subjects about Rome that relate to the city; the place. Other types are time & person.

To do a negative search on Open Library, you can use the -subject_key operator. For example, to find all the books that show up for the word "solr" that don't have the subject "Apache Solr", you would use the following search query:

https://openlibrary.org/search?q=solr+-subject_key%3A%22apache_solr%22&mode=everything

Note that the subject key is the subject name with some normalization applied (lower case, spaces converted to underscores).

Here is an example of a negative search in action:

https://openlibrary.org/search?q=machine+learning+-subject_key%3A%22python%22&mode=everything

This search will return all the books about machine learning that do not have the subject "Python".

Negative searches can be useful for finding books on a specific topic that are not limited to a particular programming language or framework. They can also be used to find books that are more general in nature.

Perform an exact search for subject using the subject_key field, e.g:
subject_key:fantasy 