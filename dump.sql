--
-- PostgreSQL database dump
--

-- Dumped from database version 13.1 (Ubuntu 13.1-1.pgdg20.04+1)
-- Dumped by pg_dump version 13.1 (Ubuntu 13.1-1.pgdg20.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: parties; Type: TABLE; Schema: public; Owner: david
--

CREATE TABLE public.parties (
    id integer NOT NULL,
    address text NOT NULL,
    city text NOT NULL,
    state text NOT NULL,
    zip_code integer NOT NULL,
    leader_id integer NOT NULL,
    name text,
    decided boolean NOT NULL,
    decided_resturaunt_id integer,
    accepting_members boolean NOT NULL
);


ALTER TABLE public.parties OWNER TO david;

--
-- Name: parties_id_seq; Type: SEQUENCE; Schema: public; Owner: david
--

CREATE SEQUENCE public.parties_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.parties_id_seq OWNER TO david;

--
-- Name: parties_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: david
--

ALTER SEQUENCE public.parties_id_seq OWNED BY public.parties.id;


--
-- Name: party_members; Type: TABLE; Schema: public; Owner: david
--

CREATE TABLE public.party_members (
    member_id integer NOT NULL,
    party_id integer NOT NULL
);


ALTER TABLE public.party_members OWNER TO david;

--
-- Name: resturaunts; Type: TABLE; Schema: public; Owner: david
--

CREATE TABLE public.resturaunts (
    id integer NOT NULL,
    name text NOT NULL,
    address text NOT NULL,
    city text NOT NULL,
    state text NOT NULL,
    zip_code integer NOT NULL,
    url text,
    party_id integer NOT NULL,
    voted_out boolean NOT NULL,
    yelp_id text,
    image_url text NOT NULL
);


ALTER TABLE public.resturaunts OWNER TO david;

--
-- Name: resturaunts_id_seq; Type: SEQUENCE; Schema: public; Owner: david
--

CREATE SEQUENCE public.resturaunts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.resturaunts_id_seq OWNER TO david;

--
-- Name: resturaunts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: david
--

ALTER SEQUENCE public.resturaunts_id_seq OWNED BY public.resturaunts.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: david
--

CREATE TABLE public.users (
    id integer NOT NULL,
    email character varying(50) NOT NULL,
    password text NOT NULL,
    name character varying(20) NOT NULL
);


ALTER TABLE public.users OWNER TO david;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: david
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO david;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: david
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: votes; Type: TABLE; Schema: public; Owner: david
--

CREATE TABLE public.votes (
    party_id integer NOT NULL,
    member_id integer NOT NULL,
    resturaunt_id integer NOT NULL,
    yay_or_nay boolean
);


ALTER TABLE public.votes OWNER TO david;

--
-- Name: parties id; Type: DEFAULT; Schema: public; Owner: david
--

ALTER TABLE ONLY public.parties ALTER COLUMN id SET DEFAULT nextval('public.parties_id_seq'::regclass);


--
-- Name: resturaunts id; Type: DEFAULT; Schema: public; Owner: david
--

ALTER TABLE ONLY public.resturaunts ALTER COLUMN id SET DEFAULT nextval('public.resturaunts_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: david
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: parties; Type: TABLE DATA; Schema: public; Owner: david
--

COPY public.parties (id, address, city, state, zip_code, leader_id, name, decided, decided_resturaunt_id, accepting_members) FROM stdin;
1	12248 Hunter's Knoll Dr	Burleson	Texas	76028	1	Valentine's day dinner	f	\N	t
\.


--
-- Data for Name: party_members; Type: TABLE DATA; Schema: public; Owner: david
--

COPY public.party_members (member_id, party_id) FROM stdin;
1	1
2	1
3	1
4	1
\.


--
-- Data for Name: resturaunts; Type: TABLE DATA; Schema: public; Owner: david
--

COPY public.resturaunts (id, name, address, city, state, zip_code, url, party_id, voted_out, yelp_id, image_url) FROM stdin;
2	Hibachio	402 E Main St	Midlothian	TX	76065	https://www.yelp.com/biz/hibachio-midlothian-2?adjust_creative=Rp1RDzDGEdqfxj94dne5aw&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=Rp1RDzDGEdqfxj94dne5aw	1	f	n5b0W-2TzWx_G9EfWJqOJQ	https://s3-media4.fl.yelpcdn.com/bphoto/lUPkBAejVGh_npKGEvcNKw/o.jpg
9	Shaneboy’s Craft Hawaiian Grindz	5731 Rendon Bloodworth Rd	Fort Worth	TX	76140	https://www.yelp.com/biz/shaneboy-s-craft-hawaiian-grindz-fort-worth?adjust_creative=Rp1RDzDGEdqfxj94dne5aw&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=Rp1RDzDGEdqfxj94dne5aw	1	f	LbeSS_mDnZYhoeyILWE7rA	https://s3-media2.fl.yelpcdn.com/bphoto/N_ezIEKQ7lSMJjiWkx0HMg/o.jpg
1	Casa Jacaranda	118 W 2nd St	Venus	TX	76084	https://www.yelp.com/biz/casa-jacaranda-venus?adjust_creative=Rp1RDzDGEdqfxj94dne5aw&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=Rp1RDzDGEdqfxj94dne5aw	1	t	5_0SD6Ny_orTKHerl1rqow	https://s3-media3.fl.yelpcdn.com/bphoto/7-bzXf6wJzUlSot5Q5AdxA/o.jpg
3	Branded Burger	100 N 8th St	Midlothian	TX	76065	https://www.yelp.com/biz/branded-burger-midlothian?adjust_creative=Rp1RDzDGEdqfxj94dne5aw&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=Rp1RDzDGEdqfxj94dne5aw	1	t	WnsNorhgDLwndoG49WVrEg	https://s3-media1.fl.yelpcdn.com/bphoto/4xq5tHbF32bFHxBscX_faA/o.jpg
4	Lighthouse Coffee Bar	1404 N 9th St	Midlothian	TX	76065	https://www.yelp.com/biz/lighthouse-coffee-bar-midlothian?adjust_creative=Rp1RDzDGEdqfxj94dne5aw&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=Rp1RDzDGEdqfxj94dne5aw	1	t	nVadJUCnOYfGLmB9Ee_iJQ	https://s3-media2.fl.yelpcdn.com/bphoto/ggtnqygo_OH1-tk_CYF21g/o.jpg
5	HideOut Burgers	1601 S 9th StSte 500	Midlothian	TX	76065	https://www.yelp.com/biz/hideout-burgers-midlothian?adjust_creative=Rp1RDzDGEdqfxj94dne5aw&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=Rp1RDzDGEdqfxj94dne5aw	1	t	-VFRpGxf6b1ueoEazdOBQw	https://s3-media1.fl.yelpcdn.com/bphoto/BMxUY-huCoMV5nP0b5ndMw/o.jpg
6	Bellucci's Italian	2000 Fm 663Ste 100	Midlothian	TX	76065	https://www.yelp.com/biz/belluccis-italian-midlothian?adjust_creative=Rp1RDzDGEdqfxj94dne5aw&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=Rp1RDzDGEdqfxj94dne5aw	1	t	th3_o7gq54n4KAXcwdNePQ	https://s3-media2.fl.yelpcdn.com/bphoto/qC_ZyHPy_SDHFtiwTriNDw/o.jpg
7	Campuzano Mexican Food	108 N 8th St	Midlothian	TX	76065	https://www.yelp.com/biz/campuzano-mexican-food-midlothian?adjust_creative=Rp1RDzDGEdqfxj94dne5aw&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=Rp1RDzDGEdqfxj94dne5aw	1	t	yvups4s-sgKJFz4Mq-d3pQ	https://s3-media4.fl.yelpcdn.com/bphoto/5225oObaYKkhYNHhalw05g/o.jpg
8	TexPlex Park	881 Miller Rd	Midlothian	TX	76065	https://www.yelp.com/biz/texplex-park-midlothian?adjust_creative=Rp1RDzDGEdqfxj94dne5aw&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=Rp1RDzDGEdqfxj94dne5aw	1	t	oga7Xxgz-vdJRx8TBv5o8w	https://s3-media4.fl.yelpcdn.com/bphoto/GMBNSM9GlvFzSmP12QfT_w/o.jpg
10	Sunrise Cafe'	104 W 2nd St	Venus	TX	76084	https://www.yelp.com/biz/sunrise-cafe-venus?adjust_creative=Rp1RDzDGEdqfxj94dne5aw&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=Rp1RDzDGEdqfxj94dne5aw	1	t	uiPOemekYZFH8r4auV-MPA	https://s3-media3.fl.yelpcdn.com/bphoto/TlI4XCK6c9EKiLswTPdHjQ/o.jpg
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: david
--

COPY public.users (id, email, password, name) FROM stdin;
1	test1@test.com	$2b$12$IqWaxlfUw.hzYmwhcDLHo.1saqgsixD47p9rI5Z6xnOEggh.uLegm	david
2	test2@test.com	$2b$12$2s7xe.kXx9/r.wQ9B4o/..RFNSXR6DBo6pGX4Fi8Qsgso2Nn/UnIG	kynsi
3	test3@test.com	$2b$12$Vb3.0S8K0mJoKbBJwHB51uIXjma2zuc5VL9sgKD7FPLCAyLM7UVde	chris
4	test4@test.com	$2b$12$qldl75n5aSGTBLXgN3cLBuee7Fa37ITU0Y8VeFpvkDew/JjQs72Xa	tori
\.


--
-- Data for Name: votes; Type: TABLE DATA; Schema: public; Owner: david
--

COPY public.votes (party_id, member_id, resturaunt_id, yay_or_nay) FROM stdin;
1	1	2	t
1	1	9	t
1	2	2	t
1	2	9	t
1	3	2	t
1	3	9	t
1	4	2	t
1	4	9	t
\.


--
-- Name: parties_id_seq; Type: SEQUENCE SET; Schema: public; Owner: david
--

SELECT pg_catalog.setval('public.parties_id_seq', 1, true);


--
-- Name: resturaunts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: david
--

SELECT pg_catalog.setval('public.resturaunts_id_seq', 10, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: david
--

SELECT pg_catalog.setval('public.users_id_seq', 4, true);


--
-- Name: parties parties_pkey; Type: CONSTRAINT; Schema: public; Owner: david
--

ALTER TABLE ONLY public.parties
    ADD CONSTRAINT parties_pkey PRIMARY KEY (id);


--
-- Name: party_members party_members_pkey; Type: CONSTRAINT; Schema: public; Owner: david
--

ALTER TABLE ONLY public.party_members
    ADD CONSTRAINT party_members_pkey PRIMARY KEY (member_id, party_id);


--
-- Name: resturaunts resturaunts_pkey; Type: CONSTRAINT; Schema: public; Owner: david
--

ALTER TABLE ONLY public.resturaunts
    ADD CONSTRAINT resturaunts_pkey PRIMARY KEY (id);


--
-- Name: resturaunts resturaunts_yelp_id_key; Type: CONSTRAINT; Schema: public; Owner: david
--

ALTER TABLE ONLY public.resturaunts
    ADD CONSTRAINT resturaunts_yelp_id_key UNIQUE (yelp_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: david
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: david
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: votes votes_pkey; Type: CONSTRAINT; Schema: public; Owner: david
--

ALTER TABLE ONLY public.votes
    ADD CONSTRAINT votes_pkey PRIMARY KEY (party_id, member_id, resturaunt_id);


--
-- Name: parties parties_leader_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: david
--

ALTER TABLE ONLY public.parties
    ADD CONSTRAINT parties_leader_id_fkey FOREIGN KEY (leader_id) REFERENCES public.users(id);


--
-- Name: party_members party_members_member_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: david
--

ALTER TABLE ONLY public.party_members
    ADD CONSTRAINT party_members_member_id_fkey FOREIGN KEY (member_id) REFERENCES public.users(id);


--
-- Name: party_members party_members_party_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: david
--

ALTER TABLE ONLY public.party_members
    ADD CONSTRAINT party_members_party_id_fkey FOREIGN KEY (party_id) REFERENCES public.parties(id);


--
-- Name: resturaunts resturaunts_party_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: david
--

ALTER TABLE ONLY public.resturaunts
    ADD CONSTRAINT resturaunts_party_id_fkey FOREIGN KEY (party_id) REFERENCES public.parties(id);


--
-- Name: votes votes_member_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: david
--

ALTER TABLE ONLY public.votes
    ADD CONSTRAINT votes_member_id_fkey FOREIGN KEY (member_id) REFERENCES public.users(id);


--
-- Name: votes votes_party_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: david
--

ALTER TABLE ONLY public.votes
    ADD CONSTRAINT votes_party_id_fkey FOREIGN KEY (party_id) REFERENCES public.parties(id);


--
-- Name: votes votes_resturaunt_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: david
--

ALTER TABLE ONLY public.votes
    ADD CONSTRAINT votes_resturaunt_id_fkey FOREIGN KEY (resturaunt_id) REFERENCES public.resturaunts(id);


--
-- PostgreSQL database dump complete
--

