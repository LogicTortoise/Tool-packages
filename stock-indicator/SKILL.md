<skill>
  <name>stock-indicator</name>
  <description>Query stock indicators (KDJ, MACD) for a given A-share symbol using AkShare and Pandas-TA.
  Usage: stock_indicator {symbol} [days]
  Example: stock_indicator 000001 5
  </description>
  <tools>
    <tool>
      <name>stock_indicator</name>
      <description>Get technical indicators (KDJ, MACD) for a stock symbol.</description>
      <parameters>
        <parameter name="symbol" type="string" required="true" description="Stock symbol (e.g., 000001, 600519)" />
        <parameter name="days" type="number" required="false" description="Number of recent days to return (default: 5)" />
      </parameters>
      <run>
        <cmd>/Users/Hht/agent-venv/bin/python /Users/Hht/.nvm/versions/node/v22.19.0/lib/node_modules/clawdbot/skills/stock-indicator/indicator.py ${symbol} --days ${days:-5}</cmd>
      </run>
    </tool>
  </tools>
</skill>
