INSERT INTO public.articles (id, title, topic, published_at) VALUES 
('a1b2c3d4-e5f6-7890-1234-56789abcdef0', 'The Future of AI in 2026', 'AI', '2026-03-01 10:00:00+00'),
('a1b2c3d4-e5f6-7890-1234-56789abcdef1', 'React Server Components Explained', 'Frontend', '2026-03-10 14:00:00+00'),
('a1b2c3d4-e5f6-7890-1234-56789abcdef2', 'Optimizing PostgreSQL Queries', 'Database', '2026-03-15 09:30:00+00'),
('a1b2c3d4-e5f6-7890-1234-56789abcdef3', 'Understanding Model Context Protocol', 'AI', '2026-03-20 11:00:00+00');

INSERT INTO public.metrics (article_id, date, views, likes, shares) VALUES
('a1b2c3d4-e5f6-7890-1234-56789abcdef0', '2026-04-01', 1200, 150, 40),
('a1b2c3d4-e5f6-7890-1234-56789abcdef0', '2026-04-02', 1500, 180, 50),
('a1b2c3d4-e5f6-7890-1234-56789abcdef0', '2026-04-03', 1100, 140, 30),
('a1b2c3d4-e5f6-7890-1234-56789abcdef0', '2026-04-04', 1600, 200, 60),

('a1b2c3d4-e5f6-7890-1234-56789abcdef1', '2026-04-01', 800, 90, 20),
('a1b2c3d4-e5f6-7890-1234-56789abcdef1', '2026-04-02', 950, 110, 25),
('a1b2c3d4-e5f6-7890-1234-56789abcdef1', '2026-04-03', 850, 100, 22),

('a1b2c3d4-e5f6-7890-1234-56789abcdef2', '2026-04-01', 600, 50, 10),
('a1b2c3d4-e5f6-7890-1234-56789abcdef2', '2026-04-02', 650, 60, 15),

('a1b2c3d4-e5f6-7890-1234-56789abcdef3', '2026-04-01', 2000, 300, 100),
('a1b2c3d4-e5f6-7890-1234-56789abcdef3', '2026-04-02', 2500, 350, 120),
('a1b2c3d4-e5f6-7890-1234-56789abcdef3', '2026-04-03', 2200, 310, 110);
