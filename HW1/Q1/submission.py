import http.client
import json
import csv

#############################################################################################################################
# cse6242 s21
# All instructions, code comments, etc. contained within this notebook are part of the assignment instructions.
# Portions of this file will auto-graded in Gradescope using different sets of parameters / data to ensure that values are not
# hard-coded.
#
# Instructions:  Implement all methods in this file that have a return
# value of 'NotImplemented'. See the documentation within each method for specific details, including
# the expected return value
#
# Helper Functions:
# You are permitted to write additional helper functions/methods or use additional instance variables within
# the `Graph` class or `TMDbAPIUtils` class so long as the originally included methods work as required.
#
# Use:
# The `Graph` class  is used to represent and store the data for the TMDb co-actor network graph.  This class must
# also provide some basic analytics, i.e., number of nodes, edges, and nodes with the highest degree.
#
# The `TMDbAPIUtils` class is used to retrieve Actor/Movie data using themoviedb.org API.  We have provided a few necessary methods
# to test your code w/ the API, e.g.: get_move_detail(), get_movie_cast(), get_movie_credits_for_person().  You may add additional
# methods and instance variables as desired (see Helper Functions).
#
# The data that you retrieve from the TMDb API is used to build your graph using the Graph class.  After you build your graph using 
# the
# TMDb API data, use the Graph class write_edges_file & write_nodes_file methods to produce the separate nodes and edges
# .csv files for use with the Argo-Lite graph visualization tool.
#
# While building the co-actor graph, you will be required to write code to expand the graph by iterating
# through a portion of the graph nodes and finding similar artists using the TMDb API. We will not grade this code directly
# but will grade the resulting graph data in your Argo-Lite graph snapshot.
#
#############################################################################################################################


class Graph:

    # Do not modify
    def __init__(self, with_nodes_file=None, with_edges_file=None):
        """
        option 1:  init as an empty graph and add nodes
        option 2: init by specifying a path to nodes & edges files
        """
        self.nodes = []
        self.edges = []
        if with_nodes_file and with_edges_file:
            nodes_CSV = csv.reader(open(with_nodes_file))
            nodes_CSV = list(nodes_CSV)[1:]
            self.nodes = [(n[0],n[1]) for n in nodes_CSV]

            edges_CSV = csv.reader(open(with_edges_file))
            edges_CSV = list(edges_CSV)[1:]
            self.edges = [(e[0],e[1]) for e in edges_CSV]


    def add_node(self, id: str, name: str)->None:
        """
        add a tuple (id, name) representing a node to self.nodes if it does not already exist
        The graph should not contain any duplicate nodes
        """
        temp_node = (id, name)
        if temp_node not in self.nodes:
            self.nodes.append(temp_node)
        return


    def add_edge(self, source: str, target: str)->None:
        """
        Add an edge between two nodes if it does not already exist.
        An edge is represented by a tuple containing two strings: e.g.: ('source', 'target').
        Where 'source' is the id of the source node and 'target' is the id of the target node
        e.g., for two nodes with ids 'a' and 'b' respectively, add the tuple ('a', 'b') to self.edges
        """

        temp_edge = (source, target)
        if temp_edge not in self.edges:
            self.edges.append(temp_edge)
        return


    def total_nodes(self)->int:
        """
        Returns an integer value for the total number of nodes in the graph
        """
        node_count = len(self.nodes)
        return node_count


    def total_edges(self)->int:
        """
        Returns an integer value for the total number of edges in the graph
        """
        edge_count = len(self.edges)
        return edge_count


    def max_degree_nodes(self)->dict:
        """
        Return the node(s) with the highest degree
        Return multiple nodes in the event of a tie
        Format is a dict where the key is the node_id and the value is an integer for the node degree
        e.g. {'a': 8}
        or {'a': 22, 'b': 22}
        """
        node_id = []
        for node in self.nodes:
            node_id.append(node[0])
        degree_count = dict.fromkeys(node_id, 0)
        for i in self.edges:
            degree_count[i[0]] += 1
            degree_count[i[1]] += 1
        #print(degree_count)
        sorted_degree_count = dict(sorted(degree_count.items(), key=lambda item: item[1], reverse=True))
        max_degree = list(sorted_degree_count.values())[0]
        degree_count = ([k for k , v in sorted_degree_count.items() if v == max_degree])

        #print(sorted_degree_count)
        #print(max_degree)
        #print(degree_count)
        degree_count = tuple(degree_count)
        print(degree_count)

        return degree_count


    def print_nodes(self):
        """
        No further implementation required
        May be used for de-bugging if necessary
        """
        print(self.nodes)


    def print_edges(self):
        """
        No further implementation required
        May be used for de-bugging if necessary
        """
        print(self.edges)


    # Do not modify
    def write_edges_file(self, path="edges.csv")->None:
        """
        write all edges out as .csv
        :param path: string
        :return: None
        """
        edges_path = path
        edges_file = open(edges_path, 'w', encoding='utf-8')

        edges_file.write("source" + "," + "target" + "\n")

        for e in self.edges:
            edges_file.write(e[0] + "," + e[1] + "\n")

        edges_file.close()
        print("finished writing edges to csv")


    # Do not modify
    def write_nodes_file(self, path="nodes.csv")->None:
        """
        write all nodes out as .csv
        :param path: string
        :return: None
        """
        nodes_path = path
        nodes_file = open(nodes_path, 'w', encoding='utf-8')

        nodes_file.write("id,name" + "\n")
        for n in self.nodes:
            nodes_file.write(n[0] + "," + n[1] + "\n")
        nodes_file.close()
        print("finished writing nodes to csv")



class  TMDBAPIUtils:

    # Do not modify
    def __init__(self, api_key:str):
        self.api_key=api_key


    def get_movie_cast(self, movie_id:str, limit:int=None, exclude_ids:list=None) -> list:
        """
        Get the movie cast for a given movie id, with optional parameters to exclude an cast member
        from being returned and/or to limit the number of returned cast members
        documentation url: https://developers.themoviedb.org/3/movies/get-movie-credits

        :param integer movie_id: a movie_id
        :param integer limit: maximum number of returned cast members by their 'order' attribute
            e.g., limit=5 will attempt to return the 5 cast members having 'order' attribute values between 0-4
            If after exluding, there are fewer cast members than the specified limit or the limit not specified, return all cast members.
            If cast members with 'order' attribute in the specified limit range have been excluded, do not include more cast members to reach the limit.
            e.g., if limit=5 and the actor whose id corresponds to cast member with order=1 is to be excluded, 
            return cast members with order values [0, 2, 3, 4], not [0, 2, 3, 4, 5]
        :param list exclude_ids: a list of ints containing ids (not cast_ids) of cast members  that should be excluded from the returned result
            e.g., if exclude_ids are [353, 455] then exclude these from any result.
        :rtype: list
            return a list of dicts, one dict per cast member with the following structure:
                [{'cast_id': '97909' # the id of the cast member
                'character': 'John Doe' # the name of the character played
                'credit_id': '52fe4249c3a36847f8012927' # id of the credit}, ... ]


        """

        """
        #Somewhat working
        
        api_link = "api.themoviedb.org/3/movie/"+str(movie_id)+"/credits?api_key="+str(self.api_key)+"&language=en-US"

        conn = http.client.HTTPSConnection(api_link)

        headers = {'Content-type': 'application/json'}

        foo = {'text': 'Hello HTTP #1 **cool**, and #1!'}
        json_data = json.dumps(foo)

        conn.request('GET', "/3/movie/"+str(movie_id)+"/credits?api_key="+str(self.api_key)+"&language=en-US")

        response = conn.getresponse()
        print(response.read().decode())
        
        #Somewhat working
        """

        # connection = http.client.HTTPSConnection(api_link)
        # connection.request("GET", "/")
        # response = connection.getresponse()
        # print(response.status)
        # print(response.reason)
        # connection.close()


        #response = connection.getresponse()
        #response.read()
        #headers = {'Content-type': 'application/json'}
        #foo = {'text': 'Hello world github/linguist#1 **cool**, and #1!'}
        #json_foo = json.dumps(foo)
        #connection.request('POST', '/markdown', json_foo, headers)
        #response = connection.getresponse()
        #response.read()
        #response = connection.getresponse()
        #print("Response: ", response)
        #connection.close()
        #cast_json = requests.get(api_link).json()
        #print(cast_json)



        """
        Instead of Using "requests" library, we have to parse json using "http.client"
        """
        # conn = http.client.HTTPSConnection("api.themoviedb.org")
        # conn.request("GET", "/3/movie/{0}/credits?api_key={1}&language=en-US".format(movie_id, self.api_key))
        # # conn.request("GET", "/3/movie/{0}?api_key={1}&language=en-US".format(movie_id, self.api_key))
        #
        # r1 = conn.getresponse()
        # movie_data = r1.read()

        # connection = http.client.HTTPSConnection("api.themoviedb.org")
        # headers = {'Content-type': 'application/json'}
        # connection.request("GET", "/3/movie/" + str(movie_id) + "/credits?api_key=" + str(self.api_key) + "&language=en-US")
        # r1 = connection.getresponse()
        # print(r1.status, r1.reason)
        #
        # if r1.status == 200:
        #     data1 = r1.read()
        #     print("DATA1: ", data1)
        # foo = {'text': 'Hello world github/linguist#1 **cool**, and #1!'}
        # json_foo = json.dumps(foo)
        # conn = http.client.HTTPSConnection("api.themoviedb.org")
        # conn.request("GET", "/3/movie/" + str(movie_id) + "/credits?api_key=" + str(self.api_key) + "&language=en-US")
        # # conn.request("GET", "/3/movie/{0}?api_key={1}&language=en-US".format(movie_id, self.api_key))
        #
        # r1 = conn.getresponse()
        # movie_data = r1.read()

        # api_link = "https://api.themoviedb.org/3/movie/" + str(movie_id) + "/credits?api_key=" + str(self.api_key) + "&language=en-US"
        # response = requests.get(api_link)
        # json_data = response.json() #json_data gets the JSON file using response.json(), instead we have to append json inside json_data using http.Client

        # conn = http.client.HTTPSConnection("api.themoviedb.org")
        # conn.request("GET", "/3/movie/" + str(movie_id) + "/credits?api_key=" + str(self.api_key) + "&language=en-US")
        # # conn.request("GET", "/3/movie/{0}?api_key={1}&language=en-US".format(movie_id, self.api_key))
        #
        # r1 = conn.getresponse()
        # json_data = r1.read()
        # # print (type(json_data))
        # # print("JSON Data: ", json_data)
        # json_data = json.loads(json_data)

        #Do not Change from here
        cast = json_data['cast']

        # :rtype: list
        #     return a list of dicts, one dict per cast member with the following structure:
        #         [{'cast_id': '97909' # the id of the cast member
        #         'character': 'John Doe' # the name of the character played
        #         'credit_id': '52fe4249c3a36847f8012927' # id of the credit}, ... ]

        #print(type(cast))
        returnlist = []
        if len(cast) >= limit and limit != None:
            for x in range(limit):
                print(cast[x])
                #print(cast[x])
                if exclude_ids != None and cast[x]['id'] not in exclude_ids :
                    item = {'cast_id':cast[x]['cast_id'], 'character':cast[x]['character'], 'credit_id': cast[x]['credit_id']}
                    returnlist.append(item)
                else:
                    item = {'cast_id':cast[x]['cast_id'], 'character':cast[x]['character'], 'credit_id': cast[x]['credit_id']}
                    returnlist.append(item)
            #print(returnlist)
        else:
            for  x in range(len(cast)):
                # print(cast[x])
                print(cast[x])
                if exclude_ids != None and cast[x]['id'] not in exclude_ids:
                    item = {'cast_id': cast[x]['cast_id'], 'character': cast[x]['character'],
                            'credit_id': cast[x]['credit_id']}
                    returnlist.append(item)
                else:
                    item = {'cast_id': cast[x]['cast_id'], 'character': cast[x]['character'],
                            'credit_id': cast[x]['credit_id']}
                    returnlist.append(item)
            # print(returnlist)


        return returnlist





    def get_movie_credits_for_person(self, person_id:str, vote_avg_threshold:float=None)->list:
        """
        Using the TMDb API, get the movie credits for a person serving in a cast role
        documentation url: https://developers.themoviedb.org/3/people/get-person-movie-credits

        :param string person_id: the id of a person
        :param vote_avg_threshold: optional parameter to return the movie credit if it is >=
            the specified threshold.
            e.g., if the vote_avg_threshold is 5.0, then only return credits with a vote_avg >= 5.0
        :rtype: list
            return a list of dicts, one dict per movie credit with the following structure:
                [{'id': '97909' # the id of the movie credit
                'title': 'Long, Stock and Two Smoking Barrels' # the title (not original title) of the credit
                'vote_avg': 5.0 # the float value of the vote average value for the credit}, ... ]
        """



        """
        Instead of Using "requests" library, we have to parse json using "http.client"
        """


        # api_link = "https://api.themoviedb.org/3/person/" + str(person_id) + "/movie_credits?api_key=" + str(self.api_key) + "&language=en-US"
        # response = requests.get(api_link)
        conn = http.client.HTTPSConnection("api.themoviedb.org")
        conn.request("GET", "/3/person/" + str(person_id) + "/movie_credits?api_key=" + str(self.api_key) + "&language=en-US")
        # conn.request("GET", "/3/movie/{0}?api_key={1}&language=en-US".format(movie_id, self.api_key))

        r1 = conn.getresponse()
        json_data = r1.read()
        print (type(json_data))
        print("JSON Data: ", json_data)
        json_data = json.loads(json_data)

        #json_data = response.json() #json_data gets the JSON file using response.json(), instead we have to append json inside json_data using http.Client
        #print(type(json_data))
        #print(json_data['cast'])

        #Do not change from here
        print("JSON_DATA: ", json_data)
        return_list = []
        for x in json_data['cast']:
            #print(x)
            if vote_avg_threshold!=None and x['vote_average'] >= vote_avg_threshold:
                item = {'id':x['id'], 'title':x['original_title'], 'vote_avg':x['vote_average']}
                return_list.append(item)
            elif vote_avg_threshold==None:
                item = {'id': x['id'], 'title': x['original_title'], 'vote_avg': x['vote_average']}
                return_list.append(item)
        print(return_list)
        return return_list

    def base_graph(self, movie_id: str, limit: int = None, exclude_ids: list = None) -> list:

        # api_link = "https://api.themoviedb.org/3/movie/" + str(movie_id) + "/credits?api_key=" + str(self.api_key) + "&language=en-US"
        # response = requests.get(api_link)
        # json_data = response.json()

        conn = http.client.HTTPSConnection("api.themoviedb.org")
        conn.request("GET", "/3/movie/" + str(movie_id) + "/credits?api_key=" + str(self.api_key) + "&language=en-US")

        r1 = conn.getresponse()
        json_data = r1.read()
        print (type(json_data))
        print("JSON Data: ", json_data)
        json_data = json.loads(json_data)


        cast = json_data['cast']


        #print(type(cast))
        returnlist = []
        if limit != None:
            if len(cast) >= limit:
                for x in range(limit):
                    # print(cast[x])
                    #print(cast[x])
                    if exclude_ids != None and cast[x]['id'] not in exclude_ids:
                        item = {'id': cast[x]['id'], 'name': cast[x]['name'],
                                'credit_id': cast[x]['credit_id']}
                        returnlist.append(item)
                    else:
                        item = {'id': cast[x]['id'], 'name': cast[x]['name'],
                                'credit_id': cast[x]['credit_id']}
                        returnlist.append(item)
                # print(returnlist)
        else:
            if exclude_ids != None and cast[x]['id'] not in exclude_ids:
                item = {'id': cast[x]['id'], 'name': cast[x]['name'],
                        'credit_id': cast[x]['credit_id']}
                returnlist.append(item)
            else:
                item = {'id': cast[x]['id'], 'name': cast[x]['name'],
                        'credit_id': cast[x]['credit_id']}
                returnlist.append(item)

        return returnlist

    def above_eight(self, person_id:str, vote_avg_threshold:float=8.0)->list:

        # api_link = "https://api.themoviedb.org/3/person/" + str(person_id) + "/movie_credits?api_key=" + str(self.api_key) + "&language=en-US"
        # response = requests.get(api_link)
        # json_data = response.json() #json_data gets the JSON file using response.json(), instead we have to append json inside json_data using http.Client

        conn = http.client.HTTPSConnection("api.themoviedb.org")
        conn.request("GET", "/3/person/" + str(person_id) + "/movie_credits?api_key=" + str(self.api_key) + "&language=en-US")

        r1 = conn.getresponse()
        json_data = r1.read()
        print (type(json_data))
        print("JSON Data: ", json_data)
        json_data = json.loads(json_data)

        return_list = []
        for x in json_data['cast']:
            if vote_avg_threshold!=None and x['vote_average'] >= vote_avg_threshold:
                item = {'id':x['id'], 'title':x['original_title'], 'vote_avg':x['vote_average']}
                return_list.append(item)
            elif vote_avg_threshold==None:
                item = {'id': x['id'], 'title': x['original_title'], 'vote_avg': x['vote_average']}
                return_list.append(item)
        return return_list

    def three_cast_members(self, movie_id: str, limit: int = None, exclude_ids: list = None) -> list:
        # api_link = "https://api.themoviedb.org/3/movie/" + str(movie_id) + "/credits?api_key=" + str(self.api_key) + "&language=en-US"
        # response = requests.get(api_link)
        # json_data = response.json()  # json_data gets the JSON file using response.json(), instead we have to append json inside json_data using http.Client

        conn = http.client.HTTPSConnection("api.themoviedb.org")
        conn.request("GET", "/3/movie/" + str(movie_id) + "/credits?api_key=" + str(self.api_key) + "&language=en-US")

        r1 = conn.getresponse()
        json_data = r1.read()
        print (type(json_data))
        print("JSON Data: ", json_data)
        json_data = json.loads(json_data)

        # Do not Change from here
        cast = json_data['cast']


        returnlist = []
        if len(cast) >= limit:
            for x in range(limit):
                #print(cast[x])
                # print(cast[x])
                if exclude_ids != None and cast[x]['id'] not in exclude_ids and int(cast[x]['order']) >= 0 and int(cast[x]['order']) <= 2:
                    item = {'id': cast[x]['id'], 'name': cast[x]['name'], 'order': cast[x]['order']}
                    returnlist.append(item)
                else:
                    if int(cast[x]['order']) >= 0 and int(cast[x]['order']) <= 2:
                        item = {'id': cast[x]['id'], 'name': cast[x]['name'], 'order': cast[x]['order']}
                        returnlist.append(item)
            # print(returnlist)
        else:
            for x in range(len(cast)):
                #print(cast[x])
                #print(cast[x])
                if exclude_ids != None and cast[x]['id'] not in exclude_ids and int(cast[x]['order']) >= 0 and int(cast[x]['order']) <= 2:
                    item = {'id': cast[x]['id'], 'name': cast[x]['name'], 'order': cast[x]['order']}
                    returnlist.append(item)
                else:
                    if int(cast[x]['order']) >= 0 and int(cast[x]['order']) <= 2:
                        item = {'id': cast[x]['id'], 'name': cast[x]['name'], 'order': cast[x]['order']}
                        returnlist.append(item)
            # print(returnlist)

        return returnlist


#############################################################################################################################
#
# BUILDING YOUR GRAPH
#
# Working with the API:  See use of http.request: https://docs.python.org/3/library/http.client.html#examples
#
# Using TMDb's API, build a co-actor network for the actor's/actress' highest rated movies
# In this graph, each node represents an actor
# An edge between any two nodes indicates that the two actors/actresses acted in a movie together
# i.e., they share a movie credit.
# e.g., An edge between Samuel L. Jackson and Robert Downey Jr. indicates that they have acted in one
# or more movies together.
#
# For this assignment, we are interested in a co-actor network of highly rated movies; specifically,
# we only want the top 3 co-actors in each movie credit of an actor having a vote average >= 8.0.
# Build your co-actor graph on the actor 'Laurence Fishburne' w/ person_id 2975.
#
# You will need to add extra functions or code to accomplish this.  We will not directly call or explicitly grade your
# algorithm. We will instead measure the correctness of your output by evaluating the data in your argo-lite graph
# snapshot.
#
# GRAPH SIZE
# With each iteration of your graph build, the number of nodes and edges grows approximately at an exponential rate.
# Our testing indicates growth approximately equal to e^2x.
# Since the TMDB API is a live database, the number of nodes / edges in the final graph will vary slightly depending on when
# you execute your graph building code. We take this into account by rebuilding the solution graph every few days and
# updating the auto-grader.  We establish a bound for lowest & highest encountered numbers of nodes and edges with a
# margin of +/- 100 for nodes and +/- 150 for edges.  e.g., The allowable range of nodes is set to:
#
# Min allowable nodes = min encountered nodes - 100
# Max allowable nodes = max allowable nodes + 100
#
# e.g., if the minimum encountered nodes = 507 and the max encountered nodes = 526, then the min/max range is 407-626
# The same method is used to calculate the edges with the exception of using the aforementioned edge margin.
# ----------------------------------------------------------------------------------------------------------------------
# BEGIN BUILD CO-ACTOR NETWORK
#
# INITIALIZE GRAPH
#   Initialize a Graph object with a single node representing Laurence Fishburne
#
# BEGIN BUILD BASE GRAPH:
#   Find all of Laurence Fishburne's movie credits that have a vote average >= 8.0
#   FOR each movie credit:
#   |   get the movie cast members having an 'order' value between 0-2 (these are the co-actors)
#   |
#   |   FOR each movie cast member:
#   |   |   using graph.add_node(), add the movie cast member as a node (keep track of all new nodes added to the graph)
#   |   |   using graph.add_edge(), add an edge between the Laurence Fishburne (actress) node
#   |   |   and each new node (co-actor/co-actress)
#   |   END FOR
#   END FOR
# END BUILD BASE GRAPH
#
#
# BEGIN LOOP - DO 2 TIMES:
#   IF first iteration of loop:
#   |   nodes = The nodes added in the BUILD BASE GRAPH (this excludes the original node of Laurence Fishburne!)
#   ELSE
#   |    nodes = The nodes added in the previous iteration:
#   ENDIF
#
#   FOR each node in nodes:
#   |  get the movie credits for the actor that have a vote average >= 8.0
#   |
#   |   FOR each movie credit:
#   |   |   try to get the 3 movie cast members having an 'order' value between 0-2
#   |   |
#   |   |   FOR each movie cast member:
#   |   |   |   IF the node doesn't already exist:
#   |   |   |   |    add the node to the graph (track all new nodes added to the graph)
#   |   |   |   ENDIF
#   |   |   |
#   |   |   |   IF the edge does not exist:
#   |   |   |   |   add an edge between the node (actor) and the new node (co-actor/co-actress)
#   |   |   |   ENDIF
#   |   |   END FOR
#   |   END FOR
#   END FOR
# END LOOP
#
# Your graph should not have any duplicate edges or nodes
# Write out your finished graph as a nodes file and an edges file using:
#   graph.write_edges_file()
#   graph.write_nodes_file()
#
# END BUILD CO-ACTOR NETWORK
# ----------------------------------------------------------------------------------------------------------------------

# Exception handling and best practices
# - You should use the param 'language=en-US' in all API calls to avoid encoding issues when writing data to file.
# - If the actor name has a comma char ',' it should be removed to prevent extra columns from being inserted into the .csv file
# - Some movie_credits may actually be collections and do not return cast data. Handle this situation by skipping these instances.
# - While The TMDb API does not have a rate-limiting scheme in place, consider that making hundreds / thousands of calls
#   can occasionally result in timeout errors. If you continue to experience 'ConnectionRefusedError : [Errno 61] Connection refused',
#   - wait a while and then try again.  It may be necessary to insert periodic sleeps when you are building your graph.


def return_name()->str:
    """
    Return a string containing your GT Username
    e.g., gburdell3
    Do not return your 9 digit GTId
    """
    return NotImplemented


def return_argo_lite_snapshot()->str:
    """
    Return the shared URL of your published graph in Argo-Lite
    """
    return NotImplemented



# You should modify __main__ as you see fit to build/test your graph using  the TMDBAPIUtils & Graph classes.
# Some boilerplate/sample code is provided for demonstration. We will not call __main__ during grading.

if __name__ == "__main__":

    graph = Graph()


    api_key = "01f03585c5e1809a42fcc3736da28ae3"


    tmdb_api_utils = TMDBAPIUtils(api_key)
    x = tmdb_api_utils.get_movie_cast(movie_id=movie_id, limit=10, exclude_ids=['819', '287'])
    print("X: ", x)
    fishburne_movies = tmdb_api_utils.get_movie_credits_for_person(person_id=2975, vote_avg_threshold=8.0)
    top_three = []
    for movie in fishburne_movies:
        id = movie['id']
        top_three.append(tmdb_api_utils.base_graph(movie_id=id, limit=3))

    nodes = []
    edges = []

    # graph.add_node(id = str(2975), name= "Laurence Fishburne")
    # nodes.append(str(2975))

    for top in top_three:
        for t in top:
            if t['id'] not in nodes:
                nodes.append(t['id'])
                graph.add_node(id=str(t['id']), name = str(t['name']))
                graph.add_edge(source=str(2975), target=str(t['id']))

    # print("GRAPH Nodes: ", graph.nodes)
    # print("graph edges: ", graph.edges)
    # print("Base Graph Complete")

    base_graph_nodes = graph.nodes.copy()
    base_graph_edges = graph.edges.copy()

    # print("Base Graph Nodes: ", base_graph_nodes)
    # print("Base Graph Edges: ", base_graph_edges)

    for node in base_graph_nodes:
        # print("Node: ", node)
        base_node_movie_creds = tmdb_api_utils.above_eight(int(node[0]))
        #print("base_node_movie_creds: \n", base_node_movie_creds)
        new_nodes = []
        new_edges = []
        for movie in base_node_movie_creds:

            movie_cast_members = tmdb_api_utils.three_cast_members(movie['id'], 3)

            for cast_member in movie_cast_members:
                if (str(cast_member['id']), cast_member['name']) not in graph.nodes:
                    graph.add_node(str(cast_member['id']), cast_member['name'])
                    new_nodes.append(cast_member['id'])
                    #print("NODE: ", node)
                    #print("CAST MEMBER: ", cast_member)



                temp_edge1 = (str(node[0]), str(cast_member['id']))
                temp_edge2 = (str(cast_member['id']), str(node[0]))
                #if temp_edge1 not in graph.edges and temp_edge2 not in graph.edges:
                if temp_edge1 not in graph.edges:
                    if temp_edge2 not in graph.edges:
                        if temp_edge1 != temp_edge2:
                            #graph.add_edge(node['id'], cast_member['id'])
                            new_edges.append((str(node[0]), cast_member['id']))
                            graph.add_edge(source=str(node[0]), target=str(cast_member['id']))

            #print("Movie cast members: ", movie_cast_members)


    # new_nodes = []
    # new_top_movies = []
    # for node in graph.nodes:
    #     print("Node: ",node)
    #     n_movies = tmdb_api_utils.above_eight(node[0], 8.0)
    #     new_top_movies.append(tmdb_api_utils.above_eight(node[0], 8.0))
    #     for movie in n_movies:
    #         new_movie_actors = tmdb_api_utils.base_graph(movie['id'], 3, nodes)
    #         print("New Movie Actors : ", new_movie_actors)
    #         if new_top_movies != []:
    #             for actor in new_movie_actors:
    #                 if actor['id'] not in nodes:
    #                     nodes.append(actor['id'])
    #                     graph.add_node(str(actor['id']), actor['name'])
    #                     graph.add_edge(str(node[0]), str(actor['id']))
    #                 elif (node[0], str(actor['id'])) not in graph.edges or (str(actor['id']), node[0]) not in graph.edges:
    #                     graph.add_edge(node[0], str(actor['id']))
    #
    # print("Edges: ", graph.edges)
    # print("Nodes: ", graph.nodes)


    # print("NEW TOP MOVIES: ", new_top_movies)
    # for new_movie in new_top_movies:
    #     print("New_Movie: ", new_movie)
    #     for nm in new_movie:
    #         new_movie_actors = tmdb_api_utils.base_graph(nm['id'], 3, nodes)
    #     print("New Movie Actors: ", new_movie_actors)









    #
    # BEGIN BUILD BASE GRAPH:
    #   Find all of Laurence Fishburne's movie credits that have a vote average >= 8.0
    #   FOR each movie credit:
    #   |   get the movie cast members having an 'order' value between 0-2 (these are the co-actors)
    #   |
    #   |   FOR each movie cast member:
    #   |   |   using graph.add_node(), add the movie cast member as a node (keep track of all new nodes added to the graph)
    #   |   |   using graph.add_edge(), add an edge between the Laurence Fishburne (actress) node
    #   |   |   and each new node (co-actor/co-actress)
    #   |   END FOR
    #   END FOR
    # END BUILD BASE GRAPH
    #
    #
    # BEGIN LOOP - DO 2 TIMES:
    #   IF first iteration of loop:
    #   |   nodes = The nodes added in the BUILD BASE GRAPH (this excludes the original node of Laurence Fishburne!)
    #   ELSE
    #   |    nodes = The nodes added in the previous iteration:
    #   ENDIF
    #
    #   FOR each node in nodes:
    #   |  get the movie credits for the actor that have a vote average >= 8.0
    #   |
    #   |   FOR each movie credit:
    #   |   |   try to get the 3 movie cast members having an 'order' value between 0-2
    #   |   |
    #   |   |   FOR each movie cast member:
    #   |   |   |   IF the node doesn't already exist:
    #   |   |   |   |    add the node to the graph (track all new nodes added to the graph)
    #   |   |   |   ENDIF
    #   |   |   |
    #   |   |   |   IF the edge does not exist:
    #   |   |   |   |   add an edge between the node (actor) and the new node (co-actor/co-actress)
    #   |   |   |   ENDIF
    #   |   |   END FOR
    #   |   END FOR
    #   END FOR
    # END LOOP
    #
    # Your graph should not have any duplicate edges or nodes
    # Write out your finished graph as a nodes file and an edges file using:
    #   graph.write_edges_file()
    #   graph.write_nodes_file()
    #
    # END BUILD CO-ACTOR NETWORK
    #print(top_three)




    # If you have already built & written out your graph, you could read in your nodes & edges files
    # to perform testing on your graph.
    #graph = Graph(with_edges_file="edges.csv", with_nodes_file="nodes.csv")

    # print(graph.nodes)
    # print(graph.edges)

    graph.write_edges_file()
    graph.write_nodes_file()