from haystack import (
  indexes as h_indexes,
)

from codepot.models.workshops import Workshop


class WorkshopIndex(h_indexes.SearchIndex, h_indexes.Indexable):
  text = h_indexes.CharField(document=True, use_template=True)

  def get_model(self):
    return Workshop

  def index_queryset(self, using=None):
    return self.get_model().objects.all()

  def prepare(self, obj):
    data = super(WorkshopIndex, self).prepare(obj)

    print(data)#TODO remove!

    return data