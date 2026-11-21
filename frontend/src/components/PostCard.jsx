import React from 'react'
import { Link } from 'react-router-dom'
export default function PostCard({post,compact=false}) {
  return <article className={`post-card ${compact?'post-card-compact':''}`}>
    <Link to={`/story/${post.slug}`} className="post-image-wrap">
      {post.cover_url?<img className="post-image" src={post.cover_url} alt={post.title}/>:<div className="image-placeholder"><i className="bi bi-journal-richtext"></i></div>}
    </Link>
    <div className="post-card-body">
      <div className="eyebrow">{post.category_name || 'Journal'} <span>·</span> {post.reading_minutes || 1} min read</div>
      <h3><Link to={`/story/${post.slug}`}>{post.title}</Link></h3>
      <p className="post-excerpt">{post.excerpt}</p>
      <div className="post-meta">
        <Link to={`/profile/${post.author?.username}`} className="author-mini">{post.author?.avatar?<img src={post.author.avatar} alt=""/>:<span>{post.author?.username?.[0]?.toUpperCase()}</span>}{post.author?.first_name ? `${post.author.first_name} ${post.author.last_name}` : post.author?.username}</Link>
        <span><i className="bi bi-heart me-1"></i>{post.like_count||0}</span>
      </div>
    </div>
  </article>
}
