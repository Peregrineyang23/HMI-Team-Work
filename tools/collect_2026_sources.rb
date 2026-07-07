#!/usr/bin/env ruby
# frozen_string_literal: true

require "json"
require "fileutils"
require "open3"
require "time"

ROOT = File.expand_path("..", __dir__)
OUT = File.join(ROOT, "tmp", "2026-source-index")
CHAT_ID = "oc_f2f29a95d46e0fcabfaff1636bbbfada"
START_DATE = Date.new(2026, 1, 1)
END_DATE = Date.new(2026, 7, 6)

FileUtils.mkdir_p(OUT)

def run_json(*argv)
  stdout, stderr, status = Open3.capture3(*argv)
  unless status.success?
    warn "FAILED: #{argv.join(" ")}"
    warn stderr
    warn stdout
    return nil
  end
  JSON.parse(stdout)
rescue JSON::ParserError => e
  warn "JSON parse failed for #{argv.join(" ")}: #{e.message}"
  warn stdout&.slice(0, 500)
  nil
end

def month_ranges(start_date, end_date)
  ranges = []
  cursor = Date.new(start_date.year, start_date.month, 1)
  while cursor <= end_date
    month_end = Date.new(cursor.year, cursor.month, -1)
    ranges << [[cursor, start_date].max, [month_end, end_date].min]
    cursor = month_end + 1
  end
  ranges
end

def collect_chat_messages
  all = []
  month_ranges(START_DATE, END_DATE).each do |from, to|
    token = nil
    page = 0
    loop do
      page += 1
      argv = [
        "lark-cli", "im", "+chat-messages-list",
        "--chat-id", CHAT_ID,
        "--start", "#{from}T00:00:00+08:00",
        "--end", "#{to}T23:59:59+08:00",
        "--order", "asc",
        "--page-size", "50",
        "--format", "json",
        "--as", "user",
        "--no-reactions"
      ]
      argv += ["--page-token", token] if token
      json = run_json(*argv)
      break unless json && json["ok"]

      data = json["data"] || {}
      messages = data["messages"] || []
      all.concat(messages)
      warn "chat #{from}..#{to} page #{page}: #{messages.length} messages"
      token = data["page_token"]
      break unless data["has_more"] && token && !token.empty?
    end
  end
  File.write(File.join(OUT, "im_messages_2026.json"), JSON.pretty_generate(all))
  all
end

def collect_drive_searches
  searches = []
  queries = [
    "",
    "红旗8397", "东风8397", "东风M18", "东风4SR", "奔腾E541",
    "车展DEMO", "AIOS", "AI workflow", "AI桌面", "fufu",
    "理想游戏", "奔驰HMI", "广汽音频", "捷途灯语",
    "设计系统", "动效平台化", "Figma", "figma"
  ]

  queries.each do |query|
    token = nil
    page = 0
    loop do
      page += 1
      argv = [
        "lark-cli", "drive", "+search",
        "--query", query,
        "--created-since", "2026-01-01",
        "--created-until", "2026-07-07",
        "--page-size", "20",
        "--format", "json",
        "--as", "user"
      ]
      argv += ["--chat-ids", CHAT_ID] if query.empty?
      argv += ["--page-token", token] if token
      json = run_json(*argv)
      break unless json && json["ok"]

      data = json["data"] || {}
      results = data["results"] || []
      searches << {"query" => query, "page" => page, "results" => results}
      warn "drive query=#{query.inspect} page #{page}: #{results.length} results"
      token = data["page_token"]
      break unless data["has_more"] && token && !token.empty? && page < 5
    end
  end
  File.write(File.join(OUT, "drive_searches_2026.json"), JSON.pretty_generate(searches))
  searches
end

def extract_figma_links(messages, searches)
  text = []
  messages.each { |m| text << m["content"].to_s }
  searches.each do |s|
    (s["results"] || []).each do |r|
      meta = r["result_meta"] || {}
      text << meta["url"].to_s
      text << r["title_highlighted"].to_s
      text << r["summary_highlighted"].to_s
    end
  end

  urls = text.join("\n").scan(%r{https?://[^\s<>"']+}).map { |u| u.gsub(/[\)\],，。]+$/, "") }.uniq
  figma = urls.select { |u| u.include?("figma.com/") }
  File.write(File.join(OUT, "figma_links_2026.json"), JSON.pretty_generate(figma))
  figma
end

messages = collect_chat_messages
searches = collect_drive_searches
figma = extract_figma_links(messages, searches)

summary = {
  generated_at: Time.now.iso8601,
  chat_messages: messages.length,
  drive_search_batches: searches.length,
  drive_results: searches.sum { |s| (s["results"] || []).length },
  figma_links: figma.length,
  output_dir: OUT
}

File.write(File.join(OUT, "collection_summary.json"), JSON.pretty_generate(summary))
puts JSON.pretty_generate(summary)
