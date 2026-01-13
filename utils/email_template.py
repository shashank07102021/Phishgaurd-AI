from datetime import datetime
from html import escape

def defang(url: str) -> str:
    """
    Make a URL non-clickable/safe for email:
    - escape HTML
    - http -> hxxp
    - . -> [.]
    """
    safe = escape(url)
    safe = safe.replace("http://", "hxxp://").replace("https://", "hxxps://")
    safe = safe.replace(".", "[.]")
    return safe

def phishing_alert_html(url: str, score: float, features: dict) -> str:
    """
    Build an HTML email body for phishing alerts (with defanged URL).
    """
    rows = "".join(
        f"<tr><td style='padding:6px;border:1px solid #333'>{escape(str(k))}</td>"
        f"<td style='padding:6px;border:1px solid #333'>{escape(str(v))}</td></tr>"
        for k, v in features.items()
    )

    return f"""
    <div style="font-family:Arial,sans-serif;max-width:640px;color:#eee;background:#121212;padding:16px">
      <h2 style="color:#ff4d4d;margin:0 0 8px">🚨 PhishGuard AI Alert</h2>

      <p style="margin:6px 0"><b>Suspicious URL (defanged):</b>
        <code style="background:#1e1e1e;padding:2px 6px;border-radius:4px">{defang(url)}</code>
        <span style="color:#ffb84d"> — DO NOT OPEN</span>
      </p>

      <p style="margin:6px 0"><b>Phishing Confidence:</b> {score:.2f}%</p>
      <p style="margin:6px 0"><b>Time:</b> {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%SZ')} (UTC)</p>

      <h3 style="margin:16px 0 8px">Feature Breakdown</h3>
      <table style="border-collapse:collapse;border:1px solid #333;background:#0f0f0f">
        <tr>
          <th style="padding:6px;border:1px solid #333;text-align:left">Feature</th>
          <th style="padding:6px;border:1px solid #333;text-align:left">Value</th>
        </tr>
        {rows}
      </table>

      <p style="font-size:12px;color:#aaa;margin-top:16px">
        This automated alert contains a defanged (non-clickable) URL for safety.
        If you believe this message is in error, mark as “Not spam” and reply to the security team.
      </p>
    </div>
    """
