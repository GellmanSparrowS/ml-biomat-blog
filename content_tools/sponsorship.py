"""Manual AdSense footer placements. Public IDs are not credentials."""
def render(language, placement):
    label = 'Sponsored links' if language == 'en' else '\u8d5e\u52a9\u5546\u94fe\u63a5'
    slot = {'home': '2013249693', 'tutorial': '7246054217'}[placement]
    return f'<aside class="site-sponsor" aria-label="{label}" hidden><p class="site-sponsor-label">{label}</p><ins class="adsbygoogle site-sponsor-unit" style="display:block" data-ad-client="ca-pub-7464969092761889" data-ad-slot="{slot}"></ins></aside>'
